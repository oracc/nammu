'''
Created on 15 Apr 2015

Main Controller class.
Initialises the controller classes and displays the view.
Handles controller events.

@author: raquel-ucl
'''

from javax.swing import JFileChooser, JOptionPane
from javax.swing.filechooser import FileNameExtensionFilter
from java.io import FileWriter, IOException
from java.lang import System, Integer
import codecs, time, os

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
        #Create this controller first since it's where the log will be displayed
        self.consoleController = ConsoleController(self)

        #TODO replace with proper Logging functionality
        self.consoleController.addText("NammuController: Creating subcontrollers...")

        #Create all the controllers
        self.menuController = MenuController(self)
        self.toolbarController = ToolbarController(self)
        self.atfAreaController = AtfAreaController(self)

        #TODO: Only if everything went fine
        self.consoleController.addText(" OK\n")

        #Log next action
        self.consoleController.addText("NammuController: Creating views...")

        #Create all the views and assigned them to appropriate controller
        self.view = NammuView(self)
        self.view.addMenuBar(self.menuController.view)
        self.view.addToolBar(self.toolbarController.view)
        self.view.addAtfArea(self.atfAreaController.view)
        self.view.addConsole(self.consoleController.view)

        self.consoleController.addText(" OK\n")

        #Log next action
        self.consoleController.addText("NammuController: Display main view...")

        #Display Nammu's view
        self.view.display()

        self.consoleController.addText(" OK\n")

        #Save current ATF filename
        #TODO: save array with all opened ATFs
        self.currentFilename = None

    #Actions delegated from subcontrollers follow.
    #Subcontrollers can't handle these actions because they
    #require interaction of several subcontrollers who have no visibility.
    #Eg. action in menu will need modification of text area controlled elsewhere
    #and not accessible from the menu controller that receives the action in the
    #first instance; or eg. show help pop up can be dealt with from
    #subcontroller

    def newFile(self, event):
        '''
        1. Check if current file in text area has unsaved changes
            1.1 Prompt user for file saving
                1.1.1 Save file
        2. Clear text area
        3. See GitHub issue: https://github.com/UCL-RITS/nammu/issues/6
        '''
        self.consoleController.addText("NammuController: Creating new file...")

        self.handleUnsaved()

        self.atfAreaController.clearAtfArea()

        self.currentFilename = None

        self.consoleController.addText(" OK\n")


    def openFile(self, event):
        '''
        1. Check if current file in text area has unsaved changes
            1.1 Prompt user for file saving
                1.1.1 Save file
        2. Display browser for user to choose file
        3. Load file in text area
        '''
        self.consoleController.addText("NammuController: Opening file...")

        self.handleUnsaved()

        fileChooser = JFileChooser()
        filter = FileNameExtensionFilter("ATF files", ["atf"])
        fileChooser.setFileFilter(filter)
        status = fileChooser.showDialog(self.view, "Choose file")

        if status == JFileChooser.APPROVE_OPTION:
            atfFile = fileChooser.getSelectedFile()
            filename = atfFile.getCanonicalPath()
            atfText = self.readTextFile(filename)
            self.currentFilename = atfFile.getCanonicalPath()
            self.atfAreaController.setAtfAreaText(atfText)

        #TODO: Else, prompt user to choose again before closing

        self.consoleController.addText(" OK\n")


    def readTextFile(self, filename):
        '''
        Helper function to open file for reading.
        '''
        text = codecs.open(filename, encoding='utf-8').read()
        return text
        #TODO: Check if selected file is ATF or at least text file!

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

        self.consoleController.addText("NammuController: Saving file...")

        fileChooser = JFileChooser()
        status = fileChooser.showSaveDialog(self.view)

        if status == JFileChooser.APPROVE_OPTION:
            atfFile = fileChooser.getSelectedFile()
            filename = atfFile.getCanonicalPath()
            atfText = self.atfAreaController.getAtfAreaText()
            self.writeTextFile(filename, atfText)
            #TODO check returned status?

        self.consoleController.addText(" OK\n")


    def writeTextFile(self, filename, text):
        '''
        Action to execute when saving an ATF.
        '''
        f = codecs.open(filename, "w", "utf-8")
        f.write(text)
        f.close()

        #TODO return status?

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
        self.consoleController.addText("NammuController: Closing file...")

        self.handleUnsaved()

        self.currentFilename = None

        self.atfAreaController.clearAtfArea()

        self.consoleController.addText(" OK\n")


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
        Helper function to decide what to do with open ATF file.
        '''
        if self.unsavedChanges():
            option = self.promptOptionPane("There are unsaved changes. Save now?")
            if option == 0:
                self.saveFile()


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

        self.handleUnsaved()

        self.consoleController.addText("NammuController: Exiting...")

        self.consoleController.addText(" OK\n")

        self.consoleController.addText("Bye! :)")

        System.exit(0)


    def undo(self, event):
        '''
        1. Check if any action happened since application was launched
        2. Come back to previous state (handle stack or rever last action)
        3. Update state stack
        Note: Check java's Undoable
        '''
        self.consoleController.addText("NammuController: Undoing last action...")

        self.consoleController.addText(" OK\n")


    def redo(self, event):
        '''
        1. Check if any action has been undone
        2. Handle actions stack and update it
        '''
        self.consoleController.addText("NammuController: Redoing last undone action...")

        self.consoleController.addText(" OK\n")


    def copy(self, event):
        '''
        Note: check if JTextArea already has this functionality
        '''
        self.consoleController.addText("NammuController: Copying selected text...")

        self.consoleController.addText(" OK\n")


    def cut(self, event):
        '''
        Note: check if JTextArea already has this functionality
        '''
        self.consoleController.addText("NammuController: Cutting selected text...")

        self.consoleController.addText(" OK\n")


    def paste(self, event):
        '''
        Note: check if JTextArea already has this functionality
        '''
        self.consoleController.addText("NammuController: Pasting clipboard text...")

        self.consoleController.addText(" OK\n")

    def validate(self, event):
        '''
        1. Parse content of text area
        2. Any errors parsing?
        3. Display OK/NOK message in Console
        '''
        # TODO Check first there is a file to be validated.
        # Also maybe ask to save before validate?
        # self.handleUnsaved()

        self.consoleController.addText("NammuController: Validating ATF file... \n")

        # Search for project name in file
        # If not found, don't validate
        # Could first try to parse, if that fails, then get it with RE by now
        project = self.get_project()
        if project:
            nammuText = self.atfAreaController.getAtfAreaText()

            # Build request.zip on the fly, pack all needed in it and send to server.
            url = 'http://oracc.museum.upenn.edu:8085'
            self.consoleController.addText("        Sending request to server at " + url + "\n")
            client = SOAPClient(url, method='POST')
            atf_basename = os.path.basename(self.currentFilename)

            client.create_request(command='atf',
                                  keys=[project, '00atf/'+atf_basename],
                                  atf_basename=atf_basename,
                                  atf_text=nammuText.encode('utf-8'))
            client.send()
            server_id = client.get_response_id()
            self.consoleController.addText("        Request sent OK with ID " + server_id + "\n")
            self.consoleController.addText("        Waiting for server to prepare response... ")

            client.wait_for_response(server_id)

            self.consoleController.addText("OK\n")

            self.consoleController.addText("        Response is ready on server. \n")
            self.consoleController.addText("        Fetching response... ")

            # This shouldn't need a new client, but a new request inside the same client
            client = SOAPClient(url, method='POST')
            client.create_request(keys=[server_id])
            client.send()

            response = client.get_response()

            self.consoleController.addText(" OK\n")


            self.consoleController.addText("        Reading response... ")
            oracc_log = client.get_oracc_log()
            self.consoleController.addText(" OK\n")

            self.consoleController.addText("        Validating ATF done. This is the log from the server:\n\n")

            self.consoleController.addText(oracc_log + "\n\n")

        else:
            self.consoleController.addText("        No project found in file. Add project and retry.\n")




        # TODO Print contents of oracc.log inside zip file. Or show in new window?

    def lemmatise(self, event):
        '''
        1. Connect with UPenn DB
        2. Send text area content
        3. Receive response file
        4. Display response in text area
        5. Display OK/NOK message in Console
        '''

        nammuText = self.atfAreaController.getAtfAreaText()

        self.consoleController.addText("NammuController: Lemmatising ATF file...")

        self.consoleController.addText(" OK\n")

    def printFile(self, event):
        '''
        Print file.
        '''
        self.consoleController.addText("NammuController: Printing file...")

        self.consoleController.addText("OK\n")

    def editSettings(self, event):
        '''
        Show settings window for edition.
        '''
        self.consoleController.addText("NammuController: Changing settings...")
        self.consoleController.addText("OK\n")


    def displayModelView(self, event):
        '''
        1. Check if a file is opened or not
        2. Check if file is valid before trying to display model view
        3. Send text to model view controller and delegate
        '''
        atfText = self.atfAreaController.getAtfAreaText()
        #if self.currentFilename != None and atfText != None :
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
        self.consoleController.addText("NammuController: Unicode...")
        self.consoleController.addText("OK\n")


    def console(self, event):
        '''
        Create bool for console, change value when clicked.
        Hide if being shown, show if hidden.
        '''
        self.consoleController.addText("NammuController: Console...")


    def toolbar(self, event):
        '''
        Show/Hide Toolbar.
        '''
        self.consoleController.addText("NammuController: Toolbar... ")
        self.consoleController.addText("OK\n")


    def __getattr__(self, name):
        '''
        Handle calls to undefined methods.
        '''
        self.consoleController.addText("!!!Undefined method " + name)

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
