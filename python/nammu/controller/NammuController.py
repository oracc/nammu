'''
Created on 15 Apr 2015

Main Controller class.
Initialises the controller classes and displays the view.
Handles controller events.

@author: raquel-ucl
'''

import codecs
import os
import logging
import logging.config
import urllib

from logging import StreamHandler, Formatter
from logging.handlers import RotatingFileHandler
from requests.exceptions import RequestException
from requests.exceptions import Timeout, ConnectionError, HTTPError

from java.io import File
from java.lang import System, Integer, ClassLoader
from javax.swing import JFileChooser, JOptionPane, ToolTipManager
from javax.swing.filechooser import FileNameExtensionFilter

from AtfAreaController import AtfAreaController
from ConsoleController import ConsoleController
from MenuController import MenuController
from ModelController import ModelController
from ToolbarController import ToolbarController

from pyoracc.atf.atffile import AtfFile
from ..SOAPClient.SOAPClient import SOAPClient
from ..utils import get_yaml_config
from ..utils.NammuConsoleHandler import NammuConsoleHandler
from ..view.NammuView import NammuView


class NammuController(object):

    def __init__(self):
        '''
        Initialise main controller of the application:
        1. For each component (menu, toolbar, ATF area, console)
            1.1 Create its controller, which will
                Create its own view referencing the corresponding controller
        2. Create main view that'll bind all the components
        3. Create event/action handlers - EventBus?
        '''
        # Create this controller first since it's where the log will be
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
        self.view.addAtfArea(self.atfAreaController.view)
        self.view.addConsole(self.consoleController.view)
        self.logger.info("Welcome to Nammu!")
        self.logger.info(
                "Please open an ATF file or start typing to create a new one.")

        # Display Nammu's view
        self.view.display()

        # Save current ATF filename
        # TODO: save array with all opened ATFs
        self.currentFilename = None

        # Configure the tooltip manager for tooltips to appear quicker and not
        # to vanish until mouse moves away
        ToolTipManager.sharedInstance().setInitialDelay(0)
        ToolTipManager.sharedInstance().setDismissDelay(Integer.MAX_VALUE)

    # Actions delegated from subcontrollers follow.
    # Subcontrollers can't handle these actions because they
    # require interaction of several subcontrollers who have no visibility.
    # Eg. action in menu will need modification of text area controlled
    # elsewhere and not accessible from the menu controller that receives the
    # action in the first instance; or eg. show help pop up can be dealt with
    # from subcontroller

    def newFile(self, event):
        '''
        1. Check if current file in text area has unsaved changes
            1.1 Prompt user for file saving
                1.1.1 Save file
        2. Clear text area
        3. See GitHub issue: https://github.com/UCL-RITS/nammu/issues/6
        '''

        if self.handleUnsaved():
            self.atfAreaController.clearAtfArea()
            self.currentFilename = None
            self.logger.debug("New file created.")

    def openFile(self, event):
        '''
        1. Check if current file in text area has unsaved changes
            1.1 Prompt user for file saving
                1.1.1 Save file
        2. Display browser for user to choose file
        3. Load file in text area
        '''

        if self.handleUnsaved():
            self.atfAreaController.clearAtfArea()

            fileChooser = JFileChooser()
            file_filter = FileNameExtensionFilter("ATF files", ["atf"])
            fileChooser.setFileFilter(file_filter)
            status = fileChooser.showDialog(self.view, "Choose file")

            filename = ''
            if status == JFileChooser.APPROVE_OPTION:
                atfFile = fileChooser.getSelectedFile()
                filename = atfFile.getCanonicalPath()
                atfText = self.readTextFile(filename)
                self.currentFilename = atfFile.getCanonicalPath()

                self.atfAreaController.setAtfAreaText(atfText)

            # TODO: Else, prompt user to choose again before closing

            # Display log only if user didn't cancel opening file action
            if filename:
                self.logger.debug("File %s successfully opened.", filename)

    def readTextFile(self, filename):
        '''
        Helper function to open file for reading.
        '''
        text = codecs.open(filename, encoding='utf-8').read()
        return text
        # TODO: Check if selected file is ATF or at least text file!

#        try:
#          reader = FileReader(f)
#          self.outer._editArea.read(reader, "")  # Use TextComponent read
#        except IOException,ioex:
#          System.out.println(e);
#          System.exit(1);

    def saveFile(self, event):
        '''
        1. Check if current file has a filename
        2. Save current file in destination given by user
        '''
        fileChooser = JFileChooser()
        status = fileChooser.showSaveDialog(self.view)

        if status == JFileChooser.APPROVE_OPTION:
            atfFile = fileChooser.getSelectedFile()
            filename = atfFile.getCanonicalPath()
            self.currentFilename = filename
            atfText = self.atfAreaController.getAtfAreaText()
            self.writeTextFile(filename, atfText)
            # TODO check returned status?

        self.logger.debug("File %s successfully saved.", filename)

    def writeTextFile(self, filename, text):
        '''
        Action to execute when saving an ATF.
        '''
        f = codecs.open(filename, "w", "utf-8")
        f.write(text)
        f.close()

        # TODO return status?

#       try:
#         writer = FileWriter(f)
#         self.outer._editArea.write(writer)  # TextComponent write
#       except IOException,ioex:
#         JOptionPane.showMessageDialog(self.outer, ioex)
#         System.exit(1)

    def closeFile(self, event):
        '''
        1. Check if file has unsaved changes
        2. Clear text area
        '''
        if self.handleUnsaved():
            self.currentFilename = None
            self.atfAreaController.clearAtfArea()
            self.logger.debug("File %s successfully closed.",
                              self.currentFilename)

    def unsavedChanges(self):
        '''
        1. Check of any file is opened
        2. Load contents in text area
        3. Load file content
        4. Check if 2 and 3 differ and return the appropriate value
        '''
        if self.currentFilename is not None:
            savedText = self.readTextFile(self.currentFilename)
            nammuText = self.atfAreaController.getAtfAreaText()

            if savedText != nammuText:
                return True
            else:
                return False

    def handleUnsaved(self):
        '''
        Helper function to decide what to do with open ATF file before having
        to clear up the text area.
        '''
        if self.unsavedChanges():
            msg = "There are unsaved changes. Save now?"
            option = self.promptOptionPane(msg)
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
        result = JOptionPane.showConfirmDialog(self.view.getContentPane(),
                                               question,
                                               "Question",
                                               JOptionPane.YES_NO_CANCEL_OPTION)
        return result

    def promptInfoPane(self, text):
        '''
        1. Show popup with given information text
        '''
        JOptionPane.showMessageDialog(self.view.getContentPane(),
                                      text,
                                      "Information",
                                      JOptionPane.INFORMATION_MESSAGE)

    def quit(self, event):
        '''
        1. Check if file has unsaved changes
        2. Exit
        '''
        if self.handleUnsaved():
            System.exit(0)

    def undo(self, event):
        self.atfAreaController.undo()

    def redo(self, event):
        self.atfAreaController.redo()

    def copy(self, event):
        self.atfAreaController.copy()

    def cut(self, event):
        self.atfAreaController.cut()

    def paste(self, event):
        self.atfAreaController.paste()

    def validate(self, event=None):
        '''
        For now, we are validating using the SOAP webservices from ORACC
        server.
        However, the intention is to replace this with validation by pyoracc.
        '''
        self.logger.debug("Validating ATF file %s.", self.currentFilename)

        # Search for project name in file. If not found, don't validate
        project = self.get_project()

        if project:
            self.send_command("atf", project)
        else:
            # TODO: Prompt dialog
            self.logger.error(
                        "No project found in file %s. Add project and retry.",
                        self.currentFilename)

        self.logger.debug("Validating ATF done.")

    def lemmatise(self, event):
        '''
        Connect to ORACC server and retrieved lemmatised version of ATF file.
        '''
        self.logger.debug("Lemmatising ATF file %s.", self.currentFilename)

        # Search for project name in file. If not found, don't validate
        project = self.get_project()

        if project:
            self.send_command("lem", project)
        else:
            # TODO: Prompt dialog.
            self.logger.error(
                            "No project found in file. Add project and retry.")

        self.logger.debug("Lemmatising ATF done.")

    def send_command(self, command, project):
        '''
        Both validation and atf validation work similarly, same for other
        services.
        This method sends a command to the ORACC server along with all the
        necessary arguments to build the HTTP request.
        '''
        # Build request.zip on the fly, pack all needed in it and send to
        # server
        # TODO: Would be nice these are read from config file.
        url = 'http://oracc.museum.upenn.edu'
        port = 8085
        url_dir = 'p'

        # Create HTTP client and prepare all input arguments for request
        client = SOAPClient(url, port, url_dir, method='POST')

        atf_basename = os.path.basename(self.currentFilename)
        nammu_text = self.atfAreaController.getAtfAreaText()

        # Send request and check for returned process ID
        client.create_request(command=command,
                              keys=[project, '00atf/'+atf_basename],
                              atf_basename=atf_basename,
                              atf_text=nammu_text.encode('utf-8'))

        try:
            self.send_request(client)
        except RequestException as re:
            self.logger.error(
                        "Error when trying to send first HTTP POST request.")
            self.logger.exception(str(re))
            return

        server_id = client.get_response_id()

        # Wait for server to prepare response
        self.logger.debug("Request sent OK with ID %s", server_id)
        self.logger.debug("Waiting for ORACC server to prepare response...")
        try:
            self.wait_for_response(client, server_id)
        except RequestException as re:
            self.logger.error("Error when trying to send HTTP GET request.")
            self.logger.exception(str(re))
            return
        except Exception as e:
            self.logger.error("Server error.")
            self.logger.exception(str(e))

        # Send new request to fetch results and server logs
        # TODO: This shouldn't need a new client, but a new request inside the
        #       same client
        # client = SOAPClient(url, port, url_dir, method='POST')
        self.logger.debug("Fetching response... ")
        client.create_request(keys=[server_id])
        try:
            self.send_request(client)
        except RequestException as re:
            msg = "Error when trying to send last HTTP POST request."
            self.logger.error(msg)
            self.logger.exception(str(re))
            return

        # Retrieve server logs and lemmatised file from server SOAP response
        self.logger.debug("Reading response sent by ORACC server... ")
        oracc_log, request_log, autolem = client.get_server_logs()
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
        if oracc_log:
            validation_errors = self.get_validation_errors(oracc_log)
            self.atfAreaController.view.error_highlight(validation_errors)
            # TODO: Prompt dialog.
            self.logger.info("The validation returned some errors: \n%s",
                             oracc_log)
            msg = "See highlighted areas in the text for errors and validate again."
            self.logger.info(msg)
        else:
            self.logger.info("The validation returned no errors.")

        if autolem:
            self.atfAreaController.setAtfAreaText(autolem.decode('utf-8'))
            self.logger.info("Lemmatised ATF received from ORACC server.")

    def send_request(self, client):
        """
        Tries to send HTTP POST request to ORACC server and raise problems.
        TODO: When we have proper logging it'd be nice to move this to the
        SOAPClient.
        # TODO: Prompt dialog when exception occurs.
        """
        try:
            client.send()
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
                msg = "Unexpected error when waiting for ORACC server to prepare response."
                self.logger.error(msg)

    def get_validation_errors(self, oracc_log):
        """
        Reads the log from the oracc server from the validation, and returns a
        dictionary with line numbers and error messages.
        """
        validation_errors = {}

        for line in oracc_log.splitlines():
            if ':' in line:
                line_number = line.split(':')[1]
                try:
                    project_id = line.split(':')[2]
                except IndexError:
                    continue
                error_message = line.split(project_id + ':')[1]
                if line_number not in validation_errors.keys():
                    validation_errors[line_number] = []
                validation_errors[line_number].append(error_message)

        validation_error_str = {}
        for line_num, errors in validation_errors.iteritems():
            error_message = "<html><font face=\"verdana\" size=\"3\">"
            for error in errors:
                error_message += "&#149; " + error + "<br/>"
            error_message += "</font></html>"
            validation_error_str[line_num] = error_message

        return validation_error_str

    def printFile(self, event):
        '''
        Print file.
        TODO: Disable this button until functionality is implemented.
        '''
        self.logger.debug("Printing file...")

    def editSettings(self, event):
        '''
        Show settings window for edition.
        TODO: ORACC Server URL should be in a config file editable from a
        settings form.
        TODO: Disable this button until functionality is implemented.
        '''
        self.logger.debug("Changing settings...")

    def displayModelView(self, event):
        '''
        1. Check if a file is opened or not
        2. Check if file is valid before trying to display model view
        3. Send text to model view controller and delegate
        '''
        atfText = self.atfAreaController.getAtfAreaText()
        # if self.currentFilename != None and atfText != None :
        if self.currentFilename is not None:
            # TODO Check if ATF is valid
            # This may imply parsing the text, so perhaps the model controller
            # can just receive the parsed object instead of the text
            self.modelController = ModelController(self, self.parse(atfText))
        else:
            self.promptInfoPane(
                        "Open ATF file before trying to display model view.")

    def parse(self, text):
        '''
        Parse input string, could be just a line or a whole file content.
        '''
        parsed = AtfFile(text)
        return parsed

    def unicode(self, event):
        '''
        Create bool for unicode, change value when clicked.
        '''
        self.logger.debug("Unicode...")

    def console(self, event):
        '''
        Create bool for console, change value when clicked.
        Hide if being shown, show if hidden.
        '''
        self.logger.debug("Console...")

    def toolbar(self, event):
        '''
        Show/Hide Toolbar.
        '''
        self.logger.debug("Toolbar... ")

    def __getattr__(self, name):
        '''
        Debug method to handle calls to undefined methods.
        Ideally this method would never be called.
        '''
        self.logger.debug("!!!Undefined method " + name)

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
                project = nammu_text.split(project_str)[1].split()[0]

        return project

    def setup_logger(self):
        """
        Creates logger for Nammu's functionality as well as to debug HTTP
        messages sent to the ORACC server and responses received.
        Output should be sent to Nammu's console as well as a local logfile and
        the system console.
        """
        yaml_dict = get_yaml_config()
        logging.config.dictConfig(yaml_dict)
        logger = logging.getLogger("NammuController")

        # create formatter and add it to the handlers
        console_handler = NammuConsoleHandler(self.consoleController)
        formatter = Formatter('%(message)s')
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)

        return logger
