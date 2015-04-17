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
import codecs, time

from ..view.NammuView import NammuView
from MenuController import MenuController
from ConsoleController import ConsoleController
from AtfAreaController import AtfAreaController
from ToolbarController import ToolbarController

class NammuController():
    
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
        
        self.menuController = MenuController(self)
        self.toolbarController = ToolbarController(self)
        self.atfAreaController = AtfAreaController(self)
        
        self.consoleController.addText(" OK\n")
        
        self.consoleController.addText("NammuController: Creating views...")
        
        self.view = NammuView(self)
        self.view.addMenuBar(self.menuController.view)
        self.view.addToolBar(self.toolbarController.view)
        self.view.addAtfArea(self.atfAreaController.view)
        self.view.addConsole(self.consoleController.view)
   
        self.consoleController.addText(" OK\n")
        
        self.consoleController.addText("NammuController: Display main view...")
        
        #Display view
        self.view.display()
    
        self.consoleController.addText(" OK\n")
    
        #Save current ATF filename 
        #TODO: save array with all opened ATFs
        self.currentFilename = None    
        
        #Handle actions - eventBus?
        
     
    #Actions delegated from subcontrollers follow. 
    #Subcontrollers can't handle these actions because they 
    #require interaction of several subcontrollers who have no visibility.
    #Eg. action in menu will need modification of text area controlled elsewhere 
    #and not accessible from the menu controller that receives the action in the
    #first instance; or eg. show help pop up can be dealt with from 
    #subcontroller)

    def newFile(self):
        """
        1. Check if current file in text area has unsaved changes
            1.1 Prompt user for file saving
                1.1.1 Save file
        2. Clear text area
        3. See GitHub issue: https://github.com/UCL-RITS/nammu/issues/6
        """
        self.consoleController.addText("NammuController: Creating new file...")
        
        if self.unsavedChanges():
            option = self.promptOptionPane("There are unsaved changes. Save now?")
            print option
            if option == 0:
                self.saveFile()
            
        self.atfAreaController.clearAtfArea()
            
        self.currentFilename = None
                
        self.consoleController.addText(" OK\n")
        
        
    def openFile(self):
        """
        1. Check if current file in text area has unsaved changes
            1.1 Prompt user for file saving
                1.1.1 Save file
        2. Display browser for user to choose file
        3. Load file in text area
        """
        self.consoleController.addText("NammuController: Opening file...")
        
        if self.unsavedChanges():
            option = self.promptOptionPane("There are unsaved changes. Save now?")
            print option
            if option == 0:
                self.saveFile()
            
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
        text = codecs.open(filename, encoding='utf-8').read()
        return text
        #TODO: Check if selected file is ATF or at least text file!

#        try:
#          reader = FileReader(f)
#          self.outer._editArea.read(reader, "")  # Use TextComponent read
#        except IOException,ioex:
#          System.out.println(e);
#          System.exit(1);
            
        
    def saveFile(self):
        """
        1. Check if current file has a filename
        2. Save current file in destination given by user
        """
        
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

        
    def closeFile(self):
        """
        1. Check if file has unsaved changes
        2. Clear text area
        """
        self.consoleController.addText("NammuController: Closing file...")
        
        if self.unsavedChanges():
            option = self.promptOptionPane("There are unsaved changes. Save now?")
            print option
            if option == 0:
                self.saveFile()
            
        self.currentFilename = None
        
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
        
            if (savedText != nammuText):
                return True
            else:
                return False
            
    def promptOptionPane(self, question):
        '''
        1. Show popup with given question text
        2. Give Yes No Cancel options
        3. Return chosen option
        '''
        result = JOptionPane.showConfirmDialog( \
                self.view.getContentPane(), question, "Question", \
                JOptionPane.YES_NO_CANCEL_OPTION)
        return result;
        
         
    def quit(self):
        """
        1. Check if file has unsaved changes
        2. Exit
        """
        self.consoleController.addText("NammuController: Exiting...")
        
        self.consoleController.addText(" OK\n")
        
        self.consoleController.addText("Bye! :)")
        
        System.exit(0)
        
    def undo(self):
        """
        1. Check if any action happened since application was launched
        2. Come back to previous state (handle stack or rever last action)
        3. Update state stack
        Note: Check java's Undoable
        """
        self.consoleController.addText("NammuController: Undoing last action...")
        
        self.consoleController.addText(" OK\n")
       
        
    def redo(self):
        """
        1. Check if any action has been undone
        2. Handle actions stack and update it
        """
        self.consoleController.addText("NammuController: Redoing last undone action...")
        
        self.consoleController.addText(" OK\n")
        
    def copy(self):
        """
        Note: check if JTextArea already has this functionality
        """
        self.consoleController.addText("NammuController: Copying selected text...")
        
        self.consoleController.addText(" OK\n")
        
    def cut(self):
        """
        Note: check if JTextArea already has this functionality
        """
        self.consoleController.addText("NammuController: Cutting selected text...")
        
        self.consoleController.addText(" OK\n") 
       
        
    def paste(self):
        """
        Note: check if JTextArea already has this functionality
        """
        self.consoleController.addText("NammuController: Pasting clipboard text...")
        
        self.consoleController.addText(" OK\n")      
        
    def validate(self, atfFile):
        """
        1. Parse content of text area
        2. Any errors parsing?
        3. Display OK/NOK message in Console
        """
        self.consoleController.addText("NammuController: Validating ATF file...")
        
        self.consoleController.addText(" OK\n")  
              
    def lemmatise(self, atfFile):
        """
        1. Connect with UPenn DB
        2. Send text area content
        3. Receive response file
        4. Display response in text area
        5. Display OK/NOK message in Console
        """
        self.consoleController.addText("NammuController: Lemmatising ATF file...")
            
        self.consoleController.addText(" OK\n") 
        
        