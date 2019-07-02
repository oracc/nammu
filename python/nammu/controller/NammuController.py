'''
Copyright 2015 - 2019 University College London.

This file is part of Nammu.

Nammu is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Nammu is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Nammu.  If not, see <http://www.gnu.org/licenses/>.
'''

import codecs
from logging import Formatter
import logging
import logging.config
import os
from swingutils.threads.swing import runSwingLater

from AtfAreaController import AtfAreaController
from ConsoleController import ConsoleController
from MenuController import MenuController
from ModelController import ModelController
from ToolbarController import ToolbarController
from NewAtfController import NewAtfController
from FindController import FindController
from EditSettingsController import EditSettingsController
from WelcomeController import WelcomeController
from java.awt import Desktop
from java.lang import System, Integer
from java.net import URI
from javax.swing import JFileChooser, JOptionPane, ToolTipManager, JSplitPane
from javax.swing.filechooser import FileNameExtensionFilter
from javax.swing.text import DefaultCaret
from pyoracc.atf.atffile import AtfFile
from requests.exceptions import RequestException, ConnectTimeout
from requests.exceptions import Timeout, ConnectionError, HTTPError

from ..SOAPClient.SOAPClient import SOAPClient
from ..utils import get_yaml_config, save_yaml_config, get_log_path
from ..utils.NammuConsoleHandler import NammuConsoleHandler
from ..view.NammuView import NammuView


class NammuController(object):
    '''
    Main Controller class.
    Initialises the controller classes and displays the view.
    Handles controller events.
    '''
    def __init__(self):
        '''
        Initialise main controller of the application:
        1. For each component (menu, toolbar, ATF area, console)
            1.1 Create its controller, which will
                Create its own view referencing the corresponding controller
        2. Create main view that'll bind all the components
        3. Create event/action handlers - EventBus?
        '''
        # Load Nammu's settings
        self.config = get_yaml_config('settings.yaml')

        # Create this controller next since it's where the log will be
        # displayed
        self.consoleController = ConsoleController(self)

        # Set up logging system
        self.logger = self.setup_logger()

        # Create all the controllers
        self.menuController = MenuController(self)
        self.toolbarController = ToolbarController(self)
        self.atfAreaController = AtfAreaController(self)

        # Create all the views and assigned them to appropriate controller
        self.view = NammuView(self)
        self.view.addMenuBar(self.menuController.view)
        self.view.addToolBar(self.toolbarController.view)
        self.view.addCenterPane(self.atfAreaController.view,
                                self.consoleController.view)
        self.logger.info("Welcome to Nammu!")
        self.logger.info(
                "You can choose an option from the menu to open an ATF or "
                "create a new one from a template, or just start typing in "
                "the text area.")

        # Display Nammu's view
        self.view.display()

        # Save current ATF filename
        # TODO: save array with all opened ATFs
        self.currentFilename = None

        # Configure the tooltip manager for tooltips to appear quicker and not
        # to vanish until mouse moves away
        ToolTipManager.sharedInstance().setInitialDelay(0)
        ToolTipManager.sharedInstance().setDismissDelay(Integer.MAX_VALUE)

        # Find windows shouldn't coexist
        self.finding = False

        # Keep track of arabic edition being on or off
        self.arabic_edition_on = False

        # Here are the current urls for nammu on github and the oracc docs
        self.urls = {'nammu': 'https://github.com/oracc/nammu',
                     'oracc': ('http://oracc.museum.upenn.edu/doc/help/'
                               'editinginatf/')}

        # Now that init is done, launch the welcome screen if needed
        self.launchWelcomeScreen()

        self.atf_body, self.atf_translation = "", ""

    # Actions delegated from subcontrollers follow.
    # Subcontrollers can't handle these actions because they
    # require interaction of several subcontrollers who have no visibility.
    # Eg. action in menu will need modification of text area controlled
    # elsewhere and not accessible from the menu controller that receives the
    # action in the first instance; or eg. show help pop up can be dealt with
    # from subcontroller

    def newFile(self, event=None):
        '''
        Checks if current file in text area has unsaved changes and prompts
        user for file saving.
        Then displays window for the user to choose ATF protocol, language and
        project, and presents a template in the text area.
        '''
        if self.handleUnsaved():
            # Open window for user to enter ATF template contents
            new_atf_controller = NewAtfController(self)
            # Keep on where we were if user doesn't cancel
            if not new_atf_controller.view.cancelled:
                self.currentFilename = None
                self.view.set_title()
                self.logger.debug("New file created from template.")

    def openFile(self, event=None):
        '''
        1. Check if current file in text area has unsaved changes
            1.1 Prompt user for file saving
                1.1.1 Save file
        2. Display browser for user to choose file
        3. Load file in text area
        4. Display file name in title bar
        '''
        if self.handleUnsaved():
            fileChooser = JFileChooser(self.get_working_dir())
            file_filter = FileNameExtensionFilter("ATF files", ["atf"])
            fileChooser.setFileFilter(file_filter)
            status = fileChooser.showDialog(self.view, "Choose file")

            if status == JFileChooser.APPROVE_OPTION:
                atfFile = fileChooser.getSelectedFile()
                self.currentFilename = atfFile.getCanonicalPath()
                atfText = self.readTextFile(self.currentFilename)
                # Clear ATF area before adding next text to clean up tooltips
                # and such
                self.atfAreaController.clearAtfArea(
                                            arabic=self.arabic_edition_on)

                # Check for Arabic content and toggle arabic translation mode
                arabicIndex = self.atfAreaController.findArabic(atfText)
                if arabicIndex:
                    self.atf_body = atfText[:arabicIndex]
                    self.atf_translation = atfText[arabicIndex:]
                    self.arabic(force=True)
                else:
                    # Turn off caret movement and highligting for file load
                    self.atfAreaController.caret.setUpdatePolicy(
                                                    DefaultCaret.NEVER_UPDATE)
                    syntax_high = self.atfAreaController.syntax_highlighter
                    syntax_high.syntax_highlight_on = True
                    self.atfAreaController.setAtfAreaText(atfText)
                    self.atf_body = atfText
                    self.atf_translation = ""
                    if self.arabic_edition_on:
                        if self.handleUnsaved():
                            self.arabic_edition_on = False
                            self.splitEditorV()

                self.consoleController.clearConsole()
                self.logger.info("File %s successfully opened.",
                                 self.currentFilename)
                self.view.set_title()

                # Re-enable caret updating and syntax highlighting after load
                self.atfAreaController.caret.setUpdatePolicy(
                                                    DefaultCaret.ALWAYS_UPDATE)

                # Now dispatch syntax highlighting in a new thread so
                # we dont highlight before the full file is loaded
                runSwingLater(self.initHighlighting)

            # TODO: Else, prompt user to choose again before closing

            # Update settings with current file's path
            self.update_config_element(self.get_working_dir(),
                                       'default', 'working_dir')

            # Finally, refresh the edit area to propagate custom font settings
            self.atfAreaController.refreshEditArea()

            # Clear stack of edits
            self.atfAreaController.undo_manager.discardAllEdits()

    def initHighlighting(self):
        '''
        A helper function to be called when we need to initialise syntax
        highlighting in a different thread.
        '''
        atfview = self.atfAreaController.view
        top, bottom = atfview.get_viewport_carets()
        self.atfAreaController.syntax_highlight(top, bottom)

    def readTextFile(self, filename):
        '''
        Helper function to open file for reading.
        '''
        if os.path.splitext(filename)[1] != '.atf':
            self.consoleController.clearConsole()
            self.logger.error("WARNING: supplied file ({}) does not appear "
                              "to be an atf file. File load may behave "
                              "unexpectedly.".format(filename))
        text = codecs.open(filename, encoding='utf-8').read()
        return text

    def _getAtfText(self, arabic_flag):
        '''
        Private method to return the atf text, concatenating the two panes if
        arabic_flag is True
        '''
        if arabic_flag:
            atfText = self.atfAreaController.concatenate_arabic_text()
        else:
            atfText = self.atfAreaController.getAtfAreaText()

        return atfText

    def saveFile(self, event=None):
        '''
        If file being edited has a path, then overwrite with latest changes.
        If file was created from scratch and has no path, prompt JFileChooser
        to save in desired location.
        Also checks for project name, and if found, makes it default.
        '''
        atfText = self._getAtfText(self.arabic_edition_on)

        if not self.currentFilename:
            fileChooser = JFileChooser(self.get_working_dir())
            file_filter = FileNameExtensionFilter("ATF files", ["atf"])
            fileChooser.setFileFilter(file_filter)
            status = fileChooser.showSaveDialog(self.view)
            if status == JFileChooser.APPROVE_OPTION:
                atfFile = fileChooser.getSelectedFile()
                filename = atfFile.getCanonicalPath()
                # Make sure users check before lightly overwriting a file
                # No need to ask if they choose to save on the file they are
                # currently and knowingly editing.
                if os.path.isfile(filename) and \
                   filename != self.currentFilename:
                    reply = JOptionPane.showConfirmDialog(
                            None,
                            "Are you sure you want to overwrite that file?",
                            "Confirm replace file",
                            JOptionPane.YES_NO_OPTION)
                    if reply == JOptionPane.NO_OPTION:
                        return
                filename = self.force_atf_extension(filename)
                self.currentFilename = filename
                self.view.set_title()
            else:
                return
        try:
            self.writeTextFile(self.currentFilename, atfText)
        except:
            self.logger.error("There was an error trying to save %s.",
                              self.currentFilename)
        else:
            self.logger.info("File %s successfully saved.",
                             self.currentFilename)

        # Find project and language and add to settings.yaml as default
        self.update_config()

    def force_atf_extension(self, filename):
        '''
        Ensures that any filename being saved has an atf extension.
        Needed as non-atf files will not validate on the oracc server
        '''
        if os.path.splitext(filename)[1] != '.atf':
            self.consoleController.clearConsole()
            self.logger.error("Supplied filename: {0} does not have the "
                              "required atf extension. File will be "
                              "saved as {0}.atf.".format(filename))
            filename = '{}.atf'.format(filename)

        return filename

    def update_config(self):
        '''
        Find project and language and add to settings.yaml as default.
        '''
        self.update_config_element(self.get_project(), 'default', 'projects')
        self.update_config_element(self.get_language(), 'default', 'languages')
        self.update_config_element(self.get_working_dir(),
                                   'default',
                                   'working_dir')

    def update_config_element(self, value, element, group):
        '''
        Update local config with given values if they are not None.
        '''
        self.logger.debug("Trying to update settings' %s with value %s.",
                          element, value)
        if value:
            if self.config[group][element] != value:
                # We need to ensure that this value is written inside a list
                # otherwise we get odd behaviour for some config files.
                if group == 'projects' and element == 'default':
                    self.config[group][element] = [value]
                else:
                    self.config[group][element] = value
                self.logger.debug("Settings updated.")
                save_yaml_config(self.config)

    def saveAsFile(self, event=None):
        '''
        Forces saving as dialog to be prompted.
        Also checks for project name, and if found, makes it default.
        '''
        atfText = self._getAtfText(self.arabic_edition_on)

        fileChooser = JFileChooser(self.get_working_dir())
        file_filter = FileNameExtensionFilter("ATF files", ["atf"])
        fileChooser.setFileFilter(file_filter)
        status = fileChooser.showSaveDialog(self.view)
        if status == JFileChooser.APPROVE_OPTION:
            atfFile = fileChooser.getSelectedFile()
            filename = atfFile.getCanonicalPath()
            # Make sure users check before lightly overwriting a file
            # No need to ask if they choose to save on the file they are
            # currently and knowingly editing.
            if os.path.isfile(filename) and filename != self.currentFilename:
                reply = JOptionPane.showConfirmDialog(
                            None,
                            "Are you sure you want to overwrite that file?",
                            "Confirm replace file",
                            JOptionPane.YES_NO_OPTION)
                if reply == JOptionPane.NO_OPTION:
                    return
            self.currentFilename = self.force_atf_extension(filename)
            self.view.set_title()
            try:
                self.writeTextFile(self.currentFilename, atfText)
            except:
                self.logger.error("There was an error trying to save %s.",
                                  self.currentFilename)
            else:
                self.logger.info("File %s successfully saved.",
                                 self.currentFilename)

        # Find project and language and add to settings.yaml as default
        self.update_config()

    def writeTextFile(self, filename, text):
        '''
        Action to execute when saving an ATF.
        '''
        try:
            f = codecs.open(filename, "w", "utf-8")
            f.write(text)
            f.close()
        except IOError as e:
            self.logger.error(str(e))
            raise

    def closeFile(self, event=None):
        '''
        1. Check if file has unsaved changes
        2. Clear text area
        '''
        if self.handleUnsaved():
            # We want to always clear the Arabic pane.
            self.atfAreaController.clearAtfArea(arabic=True)
            self.view.setTitle("Nammu")
            self.logger.debug("File %s successfully closed.",
                              self.currentFilename)
            self.currentFilename = None
            self.view.set_title()
            # Clear stack of edits
            self.atfAreaController.undo_manager.discardAllEdits()
            # Enable horizontal and vertical split only if we are not in Arabic
            # mode.
            self.menuController.enable_split_options(
                horizontal=not self.arabic_edition_on,
                vertical=not self.arabic_edition_on,
                arabic=True)

    def unsavedChanges(self):
        '''
        There are unsaved changes when the contents of the text area are
        different that those of the save file that is currently opened, and
        when the user has inserted some text and not saved it yet.
        '''
        nammuText = self._getAtfText(self.arabic_edition_on)

        if self.currentFilename:
            if os.path.isfile(self.currentFilename):
                savedText = self.readTextFile(self.currentFilename)
                if savedText != nammuText:
                    return True
                else:
                    return False
            else:
                # Clear previous log in Nammu's console and write warning
                self.consoleController.clearConsole()
                self.logger.info('{0} cannot be found.'
                                 .format(self.currentFilename))
                return True

        elif nammuText:
            return True

    def handleUnsaved(self):
        '''
        Helper function to decide what to do with open ATF file before having
        to clear up the text area.
        '''
        if self.unsavedChanges():
            option = self.promptOptionPane("There are unsaved changes. "
                                           "Save now?")
            if option == 0:
                self.saveFile()
            if option == 2:
                return False
        return True

    def promptOptionPane(self, question):
        '''
        1. Show popup with given question text
        2. Give Yes No Cancel options
        3. Return chosen option
        '''
        option = JOptionPane.YES_NO_CANCEL_OPTION
        result = JOptionPane.showConfirmDialog(self.view.getContentPane(),
                                               question,
                                               "Question",
                                               option)
        return result

    def promptInfoPane(self, text):
        '''
        1. Show popup with given information text
        '''
        JOptionPane.showMessageDialog(self.view.getContentPane(),
                                      text,
                                      "Information",
                                      JOptionPane.INFORMATION_MESSAGE)

    def quit(self, event=None):
        '''
        1. Check if file has unsaved changes
        2. Exit
        '''
        if self.handleUnsaved():
            System.exit(0)

    def undo(self, event=None):
        self.atfAreaController.undo()

    def redo(self, event=None):
        self.atfAreaController.redo()

    def copy(self, event=None):
        self.atfAreaController.copy()

    def cut(self, event=None):
        self.atfAreaController.cut()

    def paste(self, event=None):
        self.atfAreaController.paste()

    def validate(self, event=None):
        '''
        For now, we are validating using the SOAP webservices from ORACC
        server.
        However, the intention is to replace this with validation by pyoracc.
        '''
        # Clear previous log in Nammu's console
        self.consoleController.clearConsole()

        # Clear tooltips from last validation
        self.atfAreaController.clearToolTips()

        if self.currentFilename:
            # Get the file extension of the current file
            file_ext = os.path.splitext(self.currentFilename)[1]

            if file_ext == '.atf':
                self.logger.debug("Validating ATF file %s.",
                                  self.currentFilename)

                # Search for project name in file. If not found, don't validate
                project = self.get_project()

                if project:
                    self.send_command("atf", project)
                else:
                    # TODO: Prompt dialog
                    if self.currentFilename:
                        self.logger.error(
                                "No project found in file %s. "
                                "Add project and retry.",
                                self.currentFilename)
                    else:
                        self.logger.error(
                                "No project found in file %s. "
                                "Add project and retry.",
                                self.currentFilename)

                self.logger.debug("Validating ATF done.")
            else:
                self.logger.error("Unable to validate file with extension {}. "
                                  "Please re-save the file with the "
                                  "file extension .atf and try "
                                  "again.".format(file_ext))
        else:
            self.logger.error("Please save file before trying to validate.")

    def lemmatise(self, event=None):
        '''
        Connect to ORACC server and retrieved lemmatised version of ATF file.
        Don't lemmatise if file doesn't validate.
        '''
        # Grab the caret position before lemmatising
        pre_cursor = self.atfAreaController.edit_area.getCaretPosition()
        # Clear previous log in Nammu's console
        self.consoleController.clearConsole()

        # Clear tooltips from last validation
        self.atfAreaController.clearToolTips()

        if self.currentFilename:
            self.logger.debug("Lemmatising ATF file %s.", self.currentFilename)

            # Search for project name in file. If not found, don't validate
            project = self.get_project()

            if project:
                self.send_command("lem", project)
            else:
                # TODO: Prompt dialog.
                self.logger.error(
                                "No project found in file %s. "
                                "Add project and retry.",
                                self.currentFilename)

            self.logger.debug("Lemmatising ATF done.")
            # Restore the caret position following lemmatisation
            self.atfAreaController.edit_area.setCaretPosition(pre_cursor)
        else:
            self.logger.error("Please save file before trying to lemmatise.")

    def send_command(self, command, project):
        '''
        Both validation and atf validation work similarly, same for other
        services.
        This method sends a command to the ORACC server along with all the
        necessary arguments to build the HTTP request.
        '''
        # Build request.zip on the fly, pack all needed in it and send to
        # server
        server = self.config['servers']['default']
        url = self.config['servers'][server]['url']
        port = self.config['servers'][server]['port']
        url_dir = self.config['servers'][server]['dir']

        # Create HTTP client and prepare all input arguments for request
        client = SOAPClient(url, port, url_dir, method='POST')

        atf_basename = os.path.basename(self.currentFilename)
        # Do not send Arabic translation for lemmatisation.
        nammu_text = self._getAtfText(command != "lem" and
                                      self.arabic_edition_on)

        # Remove spaces from filename which make the server confused
        atf_basename = atf_basename.replace(' ', '')

        # Send request and check for returned process ID
        client.create_request(command=command,
                              keys=[project, '00atf/' + atf_basename],
                              atf_basename=atf_basename,
                              atf_text=nammu_text.encode('utf-8'))

        try:
            self.send_request(client)
        except RequestException as re:
            self.logger.error(
                        "Error when trying to send first HTTP POST request.")
            self.logger.debug(str(re))
            return
        except Exception as e:
            self.logger.debug(str(e))
            return
        server_id = client.get_response_id()

        # Wait for server to prepare response
        self.logger.debug("Request sent OK with ID %s", server_id)
        self.logger.debug("Waiting for ORACC server to prepare response...")
        try:
            self.wait_for_response(client, server_id)
        except RequestException as re:
            self.logger.error("Error when trying to send HTTP GET request.")
            self.logger.debug(str(re))
            return
        except Exception as e:
            self.logger.error("Server error.")
            self.logger.debug(str(e))
            return

        # Send new request to fetch results and server logs
        # TODO: This shouldn't need a new client, but a new request inside the
        #       same client
        # client = SOAPClient(url, port, url_dir, method='POST')
        self.logger.debug("Fetching response... ")
        client.create_request(keys=[server_id])
        try:
            self.send_request(client)
        except RequestException as re:
            self.logger.error("Error when trying to send last HTTP POST "
                              "request.")
            self.logger.exception(str(re))
            return
        except Exception as e:
            self.logger.error("Server error.")
            self.logger.debug(str(e))
            return

        # Retrieve server logs and lemmatised file from server SOAP response
        self.logger.debug("Reading response sent by ORACC server... ")
        try:
            oracc_log, request_log, autolem = client.get_server_logs()
        except IndexError:
            self.logger.error("Couldn't get server logs.")
            return
        self.process_server_response(oracc_log, request_log, autolem)

    def process_server_response(self, oracc_log, request_log, autolem):
        """
        Last HTTP POST response retrieved from server will containg at least
        two files:
          * request.log: Output log from tools run in the ORACC server like
                         ATF file unzip, etc. Logged from SOAPClient.
          * oracc.log: Validation error messages.
        If we are lemmatising, it'll also return:
          * <filename>_autolem.atf: lemmatised version of file
        """
        # Check if there were any validation errors and pass them to the
        # ATF area to refresh syntax highlighting.
        self.atfAreaController.set_validation_errors({})

        if oracc_log:
            # TODO: Prompt dialog.
            if autolem:
                self.logger.info("The lemmatisation returned some "
                                 "errors: \n")
                self.process_validation_errors(oracc_log)
            else:
                self.logger.info("The server returned some errors: \n")
                self.process_validation_errors(oracc_log)

            self.logger.info("Please, see highlighted areas and correct "
                             "errors.")

        else:
            self.logger.info("The validation returned no errors.")
            if autolem:
                self.atfAreaController.setAtfAreaText(autolem.decode('utf-8'))
                self.logger.info("Lemmatised ATF received from ORACC server.")

        # Always syntax highlight, not only when there are errors, otherwise
        # old error lines' styling won't be cleared!
        runSwingLater(self.initHighlighting)

    def send_request(self, client):
        """
        Tries to send HTTP POST request to ORACC server and raise problems.
        TODO: When we have proper logging it'd be nice to move this to the
        SOAPClient.
        # TODO: Prompt dialog when exception occurs.
        """
        try:
            client.send()
        except (Timeout, ConnectTimeout):
            self.logger.error('ORACC %s server timed out after 5 seconds.',
                              client.url)
            self.logger.error('You can try with a different server from the '
                              'settings menu.')
            raise Exception('Connection to server {} timed '
                            'out.'.format(client.url))
        except ConnectionError:
            raise Exception("Can't connect to ORACC server at %s.",
                            client.url)
        except HTTPError:
            raise Exception("ORACC server returned invalid HTTP response.")

    def wait_for_response(self, client, server_id):
        """
        Tries to send HTTP GET request to ORACC server and raise problems.
        TODO: When we have proper logging it'd be nice to move this to the
        SOAPClient.
        # TODO: Prompt dialog when exception occurs.
        """
        try:
            client.wait_for_response(server_id)
        except Timeout:
            self.logger.error("ORACC server timed out after 5 seconds.")
            raise
        except ConnectionError:
            self.logger.error("Can't connect to ORACC server at %s.",
                              client.url)
            raise
        except HTTPError:
            self.logger.error("ORACC server returned invalid HTTP response.")
            raise
        except Exception as e:
            if e.args == "UnknownServerError":
                self.logger.error(
                            "ORACC server seems down. Contact server admin.")
                raise
            else:
                self.logger.error("Unexpected error when waiting for ORACC "
                                  "server to prepare response.")

    def process_validation_errors(self, oracc_log):
        """
        Reads the log from the oracc server from the validation, and refreshes
        the dictionary with line numbers and error messages.
        """
        validation_errors = {}
        for line in oracc_log.splitlines():
            if ':' in line:
                try:
                    server_filename = line.split(':')[0]
                    line_number = line.split(':')[1]
                    project_id = line.split(':')[2]
                    error_message = line.split(project_id + ':')[1]
                except IndexError:
                    continue

                if line_number not in validation_errors.keys():
                    validation_errors[line_number] = ''

                formatted_err = ('<a href={0}>{1}:{0}</a>:{2}:{3}'
                                 .format(line_number,
                                         server_filename,
                                         project_id,
                                         error_message))
                validation_errors[line_number] += formatted_err
                self.logger.info(formatted_err)
            else:
                summary_line = line

        # Finally, write the servers summary line to the logger
        self.logger.info(summary_line)

        # Refresh validation errors
        self.atfAreaController.set_validation_errors(validation_errors)

    def launchWelcomeScreen(self):
        '''
        Checks if new_user flag is true, launches the welcome screen if needed
        '''
        if self.config.get('new_user', True):
            WelcomeController(self).view.display()

    def printFile(self, event=None):
        '''
        Print file.
        TODO: Disable this button until functionality is implemented.
        '''
        self.logger.debug("Printing file...")

    def editSettings(self, event=None):
        '''
        Show settings window for edition.
        '''
        # Clear console in preparation for new settings messages
        self.consoleController.clearConsole()

        EditSettingsController(self).view.display()

    def displayModelView(self, event=None):
        '''
        1. Check if a file is opened or not
        2. Check if file is valid before trying to display model view
        3. Send text to model view controller and delegate
        '''
        atfText = self.atfAreaController.getAtfAreaText()
        if self.currentFilename or atfText:
            # TODO Check if ATF is valid
            # This may imply parsing the text, so perhaps the model controller
            # can just receive the parsed object instead of the text
            self.modelController = ModelController(self, self.parse(atfText))
        else:
            self.promptInfoPane(
                        "Open ATF file before trying to display model view.")

    def parse(self, text, event=None):
        '''
        Parse input string, could be just a line or a whole file content.
        '''
        try:
            parsed = AtfFile(text)
        except SyntaxError as e:
            self.logger.error("There is a syntax error near character '{}' "
                              "in line {} and position {}".format(
                                                        e.text.strip('\n'),
                                                        e.lineno,
                                                        e.offset + 1)
                              )
        else:
            return parsed

    def arabic(self, event=None, force=False):
        '''
        Create bool for arabic, change value when clicked.

        If `force` is `True`, force enabling arabic mode.
        '''
        if force:
            self.logger.debug("Enabling Arabic translation mode...")
            atfAreaView = self.atfAreaController.view
            atfAreaView.edit_area.setText(self.atf_body)
            atfAreaView.arabic_area.setText(self.atf_translation)
            atfAreaView.setup_edit_area_split(JSplitPane.VERTICAL_SPLIT,
                                              arabic=True)
            self.menuController.enable_split_options(
                horizontal=False, vertical=False, arabic=False)
            return
        self.logger.debug("Enabling/Disabling arabic translation mode...")
        if event:
            if self.handleUnsaved():
                if self.arabic_edition_on:
                    # revert back to single pane
                    joined = self.atfAreaController.concatenate_arabic_text()
                    if self.atfAreaController.findArabic(joined):
                        self.logger.info("Cannot disable Arabic translation"
                                         " mode, Arabic translation detected")
                    else:
                        self.atfAreaController.view.toggle_split()
                        self.arabic_edition_on = False
                        self.atfAreaController.edit_area.setText(joined)

                else:
                    # toggle arabic pane
                    self.atfAreaController.splitEditorArabic(
                                    JSplitPane.VERTICAL_SPLIT,
                                    self.atfAreaController.getAtfAreaText(),
                                    "")
        else:
            self.atfAreaController.splitEditorArabic(JSplitPane.VERTICAL_SPLIT,
                                                     self.atf_body,
                                                     self.atf_translation)
            self.menuController.enable_split_options(
                horizontal=False, vertical=False, arabic=False)

    def splitEditorV(self, event=None):
        '''
        Show/hide vertical split editor.
        '''
        self.logger.debug("Split Editor Vertically...")
        self.atfAreaController.splitEditor(JSplitPane.VERTICAL_SPLIT)

    def splitEditorH(self, event=None):
        '''
        Show/hide horizontal split editor.
        '''
        self.logger.debug("Split Editor Horizontally...")
        self.atfAreaController.splitEditor(JSplitPane.HORIZONTAL_SPLIT)

    def console(self, event=None):
        '''
        Create bool for console, change value when clicked.
        Hide if being shown, show if hidden.
        '''
        self.logger.debug("Console...")

    def toolbar(self, event=None):
        '''
        Show/Hide Toolbar.
        '''
        self.logger.debug("Toolbar... ")

    def unicode(self, event=None):
        '''
        Create bool for unicode, change value when clicked.
        '''
        self.logger.debug("Unicode...")

    def __getattr__(self, name):
        '''
        Debug method to handle calls to undefined methods.
        Ideally this method would never be called.
        '''
        self.logger.debug("Undefined method " + name)

    def get_project(self):
        '''
        Search for project in text content.
        First try to parse it and get it from the parser.
        If that fails, try to find it with re ("#project: xxxx").
        If that fails as well, display error message and ask for project.
        '''
        project = None
        project_str = "#project:"

        nammu_text = self.atfAreaController.getAtfAreaText()

        if project_str in nammu_text:
            try:
                parsed_atf = self.parse(nammu_text)
                project = parsed_atf.text.project
            except:
                # File can't be parsed but might still contain a project code
                try:
                    project = nammu_text.split(project_str)[1].split()[0]
                except IndexError:
                    self.logger.error("Project format should be "
                                      "'#project: xxx/xxx'.")

        return project

    def get_language(self):
        '''
        Search for language protocol in text content.
        First try to parse it and get it from the parser.
        If that fails, try to find it with re ("#atf: lang xxxx").
        If that fails as well, ignore.
        '''
        language = None
        lang_value = None
        lang_str = "#atf: lang"

        nammu_text = self.atfAreaController.getAtfAreaText()

        if lang_str in nammu_text:
            try:
                parsed_atf = self.parse(nammu_text)
                lang_value = getattr(parsed_atf.text, 'language')
            except:
                # File can't be parsed but might still contain a project code
                try:
                    lang_value = nammu_text.split(lang_str)[1].split()[0]
                except IndexError:
                    pass

        # We need to return the dictionary key and not the value :S
        for key, value in self.config['languages'].iteritems():
            if value == lang_value:
                language = key

        return language

    def get_working_dir(self):
        '''
        Look up working dir where the current ATF file is.
        If it's a new file, use default working_dir from settings.
        If all else fails, set up working dir to current dir from which Nammu
        was opened.
        '''
        if self.currentFilename:
            working_dir = os.path.dirname(self.currentFilename)
        else:
            try:
                working_dir = self.config['working_dir']['default']
            except KeyError:
                working_dir = os.getcwd()
        return working_dir

    def setup_logger(self):
        """
        Creates logger for Nammu's functionality as well as to debug HTTP
        messages sent to the ORACC server and responses received.
        Output should be sent to Nammu's console as well as a local logfile
        and the system console.
        """
        yaml_dict = get_yaml_config('logging.yaml')
        # Replace user given basename with absolute path to log file
        logfile = yaml_dict['handlers']['file_handler']['filename']
        yaml_dict['handlers']['file_handler']['filename'] = get_log_path(
                                                                    logfile)
        logging.config.dictConfig(yaml_dict)
        logger = logging.getLogger("NammuController")

        # create formatter and add it to the handlers
        console_handler = NammuConsoleHandler(self.consoleController)
        formatter = Formatter('%(message)s')
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)

        return logger

    def showHelp(self, event=None):
        """
        Show ATF validation help.
        """
        self._open_website(self.urls['oracc'])

    def showAbout(self, event=None):
        """
        Show repo's website with info about ORACC and Nammu.
        """
        self._open_website(self.urls['nammu'])

    def _open_website(self, url):
        uri = URI(url)
        desktop = None
        if Desktop.isDesktopSupported():
            desktop = Desktop.getDesktop()
        if desktop and desktop.isSupported(Desktop.Action.BROWSE):
            desktop.browse(uri)

    def find(self, event=None):
        '''
        Find/Replace functionality:
        * Displays find/replace window with options
        * Highlights matches
        * Replaces matches on text
        '''
        if self.find_controller:
            if not self.find_controller.view.isShowing():
                self.find_controller = FindController(self)
        else:
            self.find_controller = FindController(self)
