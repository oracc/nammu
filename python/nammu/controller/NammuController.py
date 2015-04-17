'''
Created on 15 Apr 2015

Main Controller class. 
Initialises the controller classes and displays the view.
Handles controller events.

@author: raquel-ucl
'''

from javax.swing import JFileChooser
from javax.swing.filechooser import FileNameExtensionFilter
from java.io import FileWriter, IOException
from java.lang import System, Integer

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
        
        self.menuController = MenuController(self)
        self.toolbarController = ToolbarController(self)
        self.atfAreaController = AtfAreaController(self)
        self.consoleController = ConsoleController(self)
    
        self.view = NammuView(self)
        self.view.addMenuBar(self.menuController.view)
        self.view.addToolBar(self.toolbarController.view)
        self.view.addAtfArea(self.atfAreaController.view)
        self.view.addConsole(self.consoleController.view)
   
        #Display view
        self.view.display()
        
        #Handle actions - eventBus?
        
     
    #Actions delegated from subcontrollers follow. 
    #Subcontrollers can't handle these actions because they 
    #require interaction of several subcontrollers who have no visibility.
    #Eg. action in menu will need modification of text area controlled elsewhere 
    #and not accessible from the menu controller that receives the action in the
    #first instance; or eg. show help pop up can be dealt with from 
    #subcontroller)

    def newFile(self):
        print "Creating new file from controller"
        """
        1. Check if current file in text area has unsaved changes
            1.1 Prompt user for file saving
                1.1.1 Save file
        2. Clear text area
        3. See GitHub issue: https://github.com/UCL-RITS/nammu/issues/6
        """
        
        
    def openFile(self):
        print "Opening file from controller"
        """
        1. Check if current file in text area has unsaved changes
            1.1 Prompt user for file saving
                1.1.1 Save file
        2. Display browser for user to choose file
        3. Load file in text area
        """
        
        fileChooser = JFileChooser()
        filter = FileNameExtensionFilter("ATF files", ["atf"])
        fileChooser.setFileFilter(filter)
        status = fileChooser.showDialog(self.view, "Choose file")
        

        if status == JFileChooser.APPROVE_OPTION:
            atfFile = fileChooser.getSelectedFile()
            atfText = self.readTextFile(atfFile)
            self.atfAreaController.setAtfAreaText(atfText)
            print atfText
        
        #TODO: Else, prompt user to choose again before closing

    
    def readTextFile(self, file):
        filename = file.getCanonicalPath()
        f = open(filename, "r")
        text = f.read()
        return text
        #TODO: Check if selected file is ATF or at least text file!

#        try:
#          reader = FileReader(f)
#          self.outer._editArea.read(reader, "")  # Use TextComponent read
#        except IOException,ioex:
#          System.out.println(e);
#          System.exit(1);
            
        
    def saveFile(self):
        print "Saving file from controller"
        """
        1. Save current file
        """
       
        
#     retval = self.outer._fileChooser.showSaveDialog(self.outer)
#     if retval == JFileChooser.APPROVE_OPTION:
#       f = self.outer._fileChooser.getSelectedFile()
#       try:
#         writer = FileWriter(f)
#         self.outer._editArea.write(writer)  # TextComponent write
#       except IOException,ioex:
#         JOptionPane.showMessageDialog(self.outer, ioex)
#         System.exit(1)

         
    def closeFile(self):
        print "Closing file from controller"
        """
        1. Check if file has unsaved changes
        2. Clear text area
        """
       
    
    def quit(self):
        print "Exiting from controller"
        """
        1. Check if file has unsaved changes
        2. Exit
        """
        System.exit(0)
        
    def undo(self):
        print "Undoing from controller"
        """
        1. Check if any action happened since application was launched
        2. Come back to previous state (handle stack or rever last action)
        3. Update state stack
        Note: Check java's Undoable
        """
       
        
    def redo(self):
        print "Redoing from controller"
        """
        1. Check if any action has been undone
        2. Handle actions stack and update it
        """
       
        
    def copy(self):
        print "Copying from controller"
        """
        Note: check if JTextArea already has this functionality
        """
        
        
    def cut(self):
        print "Cutting from controller"
        """
        Note: check if JTextArea already has this functionality
        """
       
        
    def paste(self):
        print "Pasting from controller"
        """
        Note: check if JTextArea already has this functionality
        """
      
        
    def validate(self, atfFile):
        print "Validating from controller"
        """
        1. Parse content of text area
        2. Any errors parsing?
        3. Display OK/NOK message in Console
        """
       
        
    def lemmatise(self, atfFile):
        print "Lemmatising from controller"
        """
        1. Connect with UPenn DB
        2. Send text area content
        3. Receive response file
        4. Display response in text area
        5. Display OK/NOK message in Console
        """
        