'''
Created on 15 Apr 2015

Main Controller class.
Initialises the controller classes and displays the view.
Handles controller events.

@author: raquel-ucl
'''

from javax.swing import JFileChooser, JOptionPane, ToolTipManager
from javax.swing.filechooser import FileNameExtensionFilter
from java.lang import System, Integer

import codecs, os
from pyoracc.atf.atffile import AtfFile
from ..view.NammuView import NammuView
from MenuController import MenuController
from ConsoleController import ConsoleController
from AtfAreaController import AtfAreaController
from ToolbarController import ToolbarController
from ModelController import ModelController
from ..SOAPClient.SOAPClient import SOAPClient

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
        # Create this controller first since it's where the log will be displayed
        self.consoleController = ConsoleController(self)

        # TODO replace with proper Logging functionality
        self.log("NammuController: Creating subcontrollers...")

        # Create all the controllers
        self.menuController = MenuController(self)
        self.toolbarController = ToolbarController(self)
        self.atfAreaController = AtfAreaController(self)

        # TODO: Only if everything went fine
        self.log(" OK\n")

        # Log next action
        self.log("NammuController: Creating views...")

        # Create all the views and assigned them to appropriate controller
        self.view = NammuView(self)
        self.view.addMenuBar(self.menuController.view)
        self.view.addToolBar(self.toolbarController.view)
        self.view.addAtfArea(self.atfAreaController.view)
        self.view.addConsole(self.consoleController.view)
        self.log(" OK\n")

        # Log next action
        self.log("NammuController: Display main view...")

        # Display Nammu's view
        self.view.display()

        self.log(" OK\n")

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
    # Eg. action in menu will need modification of text area controlled elsewhere
    # and not accessible from the menu controller that receives the action in the
    # first instance; or eg. show help pop up can be dealt with from
    # subcontroller

    def newFile(self, event):
        '''
        1. Check if current file in text area has unsaved changes
            1.1 Prompt user for file saving
                1.1.1 Save file
        2. Clear text area
        3. See GitHub issue: https://github.com/UCL-RITS/nammu/issues/6
        '''

        if self.handleUnsaved():
            self.log("NammuController: Creating new file...")
            self.atfAreaController.clearAtfArea()
            self.currentFilename = None
            self.log(" OK\n")


    def openFile(self, event):
        '''
        1. Check if current file in text area has unsaved changes
            1.1 Prompt user for file saving
                1.1.1 Save file
        2. Display browser for user to choose file
        3. Load file in text area
        '''

        if self.handleUnsaved():
            self.log("NammuController: Opening file...")

            self.atfAreaController.clearAtfArea()


            fileChooser = JFileChooser()
            file_filter = FileNameExtensionFilter("ATF files", ["atf"])
            fileChooser.setFileFilter(file_filter)
            status = fileChooser.showDialog(self.view, "Choose file")

            if status == JFileChooser.APPROVE_OPTION:
                atfFile = fileChooser.getSelectedFile()
                filename = atfFile.getCanonicalPath()
                atfText = self.readTextFile(filename)
                self.currentFilename = atfFile.getCanonicalPath()

                self.atfAreaController.setAtfAreaText(atfText)

            # TODO: Else, prompt user to choose again before closing

            self.log(" OK\n")


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

        self.log("NammuController: Saving file...")

        fileChooser = JFileChooser()
        status = fileChooser.showSaveDialog(self.view)

        if status == JFileChooser.APPROVE_OPTION:
            atfFile = fileChooser.getSelectedFile()
            filename = atfFile.getCanonicalPath()
            atfText = self.atfAreaController.getAtfAreaText()
            self.writeTextFile(filename, atfText)
            #TODO check returned status?

        self.log(" OK\n")


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
            self.log("NammuController: Closing file...")
            self.currentFilename = None
            self.atfAreaController.clearAtfArea()
            self.log(" OK\n")


    def unsavedChanges(self):
        '''
        1. Check of any file is opened
        2. Load contents in text area
        3. Load file content
        4. Check if 2 and 3 differ and return the appropriate value
        '''
        if self.currentFilename != None:
            savedText = self.readTextFile(self.currentFilename)
            nammuText = self.atfAreaController.getAtfAreaText()

            if savedText != nammuText:
                return True
            else:
                return False


    def handleUnsaved(self):
        '''
        Helper function to decide what to do with open ATF file before having to
        clear up the text area.
        '''
        if self.unsavedChanges():
            option = self.promptOptionPane("There are unsaved changes. Save now?")
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
        result = JOptionPane.showConfirmDialog( \
                self.view.getContentPane(), question, "Question", \
                JOptionPane.YES_NO_CANCEL_OPTION)
        return result


    def promptInfoPane(self, text):
        '''
        1. Show popup with given information text
        '''
        JOptionPane.showMessageDialog( \
                self.view.getContentPane(), text, "Information", \
                JOptionPane.INFORMATION_MESSAGE)


    def quit(self, event):
        '''
        1. Check if file has unsaved changes
        2. Exit
        '''

        if self.handleUnsaved():
            self.log("NammuController: Exiting...")
            self.log(" OK\n")
            self.log("Bye! :)")
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
        For now, we are validating using the SOAP webservices from ORACC server.
        However, the intention is to replace this with validation by pyoracc.
        '''
        self.log("NammuController: Validating ATF file... \n")

        # Search for project name in file. If not found, don't validate
        project = self.get_project()

        if project:
            self.send_command("atf", project)
        else:
            self.log("        No project found in file. Add project and retry.\n")

        self.log("        Validating ATF done.\n")


    def lemmatise(self, event):
        '''
        Connect to ORACC server and retrieved lemmatised version of ATF file.
        '''
        self.log("NammuController: Lemmatising ATF file... \n")

        # Search for project name in file. If not found, don't validate
        project = self.get_project()

        if project:
            self.send_command("lem", project)
        else:
            self.log("        No project found in file. Add project and retry.\n")


    def send_command(self, command, project):
        '''
        Both validation and atf validation work similarly, same for other
        services.
        This method sends a command to the ORACC server along with all the
        necessary arguments to build the HTTP request.
        '''

        # Build request.zip on the fly, pack all needed in it and send to server.
        url = 'http://oracc.museum.upenn.edu'
        port = 8085
        url_dir = 'p'
        
        self.log("        Sending request to server at " + url + "\n")

        # Create HTTP client and prepare all input arguments for request
        client = SOAPClient(url, port, url_dir, method='POST')
        atf_basename = os.path.basename(self.currentFilename)
        nammuText = self.atfAreaController.getAtfAreaText()

        # Send request and check for returned process ID
        client.create_request(command=command,
                              keys=[project, '00atf/'+atf_basename],
                              atf_basename=atf_basename,
                              atf_text=nammuText.encode('utf-8'))
        client.send()
        server_id = client.get_response_id()

        # Wait for server to prepare response
        self.log("        Request sent OK with ID " + server_id + "\n")
        self.log("        Waiting for server to prepare response... ")
        client.wait_for_response(server_id)
        self.log("OK\n")
        self.log("        Fetching response... ")

        # Send new request to fetch results and server logs
        # This shouldn't need a new client, but a new request inside the same client
        client = SOAPClient(url, port, url_dir, method='POST')
        client.create_request(keys=[server_id])
        client.send()
        response = client.get_response()
        self.log(" OK\n")
        self.log("        Reading response... ")
        oracc_log, request_log, autolem = client.get_server_logs()
        self.log(" OK\n")

        if autolem:
            self.atfAreaController.setAtfAreaText(autolem)
            self.log("        Lemmatised ATF received from server.\n")

        if oracc_log:
            validation_errors = self.get_validation_errors(oracc_log)
            self.atfAreaController.view.error_highlight(validation_errors)
            self.log("        See highlighted areas in the text for errors and check again.\n\n")
        else:
            self.log("        The ORACC server didn't report any validation errors.\n\n")

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
        '''
        self.log("NammuController: Printing file...")

        self.log("OK\n")


    def editSettings(self, event):
        '''
        Show settings window for edition.
        '''
        self.log("NammuController: Changing settings...")
        self.log("OK\n")


    def displayModelView(self, event):
        '''
        1. Check if a file is opened or not
        2. Check if file is valid before trying to display model view
        3. Send text to model view controller and delegate
        '''
        atfText = self.atfAreaController.getAtfAreaText()
        # if self.currentFilename != None and atfText != None :
        if self.currentFilename != None:
            #TODO Check if ATF is valid
            #This may imply parsing the text, so perhaps the model controller
            #can just receive the parsed object instead of the text
            self.modelController = ModelController(self, self.parse(atfText))
        else:
            self.promptInfoPane("Open ATF file before trying to display model view.")


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
        self.log("NammuController: Unicode...")
        self.log("OK\n")


    def console(self, event):
        '''
        Create bool for console, change value when clicked.
        Hide if being shown, show if hidden.
        '''
        self.log("NammuController: Console...")


    def toolbar(self, event):
        '''
        Show/Hide Toolbar.
        '''
        self.log("NammuController: Toolbar... ")
        self.log("OK\n")


    def __getattr__(self, name):
        '''
        Handle calls to undefined methods.
        '''
        self.log("!!!Undefined method " + name)


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
            except SyntaxError:
                # File can't be parsed but might still contain a project code
                project = nammu_text.split(project_str)[1].split()[0]

        return project


    def log(self, string):
        '''
        By now we are outputting in the console directly. A better logging
        method would be nice though.
        '''
        self.consoleController.addText(string)
