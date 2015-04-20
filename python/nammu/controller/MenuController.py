'''
Created on 15 Apr 2015

Creates the menu view and handles menu actions.

@author: raquel-ucl
'''

from ..view.MenuView import MenuView

class MenuController():
    
    def __init__(self, mainController):
        print "I'm the menu controller"
        
        #Create view with a reference to its controller to handle events
        self.view = MenuView(self)
        
        #Will also need delegating to parent presenter
        self.controller = mainController
        
    #Actions delegated from view. Some of them will need delegation to app
    #controller (eg. action in menu will need modification of text area 
    #controlled elsewhere and not accessible from this controller; eg. quit 
    #Nammu or show help pop up can be dealt with from here)

    def newFile(self):
        self.controller.newFile()
        
    def openFile(self):
        self.controller.openFile()
        
    def saveFile(self):
        self.controller.saveFile()

    def closeFile(self):
        self.controller.closeFile()
    
    def printFile(self):
        self.controller.printFile()
        
    def quit(self):
        self.controller.quit()
        
    def undo(self):
        self.controller.undo()
        
    def redo(self):
        self.controller.redo()
        
    def copy(self):
        self.controller.copy()
        
    def cut(self):
        self.controller.cut()
        
    def paste(self):
        self.controller.paste()
        
    def validate(self, atfFile):
        self.controller.validate(atfFile)
        
    def lemmatise(self, atfFile):
        self.controller.lemmatise(atfFile)
        
    def editSettings(self):
        """
        Show settings window for edition.
        """
        self.controller.editSettings()
        
    def showHelp(self):
        """ 
        1. Show popup window with help (or just open firefox with ORACC info?)
        """
        
    def showAbout(self):
        """ 
        1. Show popup window with help (or just open firefox with ORACC info?)
        """
        
    def displayModelView(self):
        """
        1. Parse text area content
        2. Change atfArea mode to model view
        3. Process parsed data and serialize in separate JPanel
        4. Think about whether the other user options should remain visible or
        should this just be shown in a separate window?
        """
        self.controller.displayModelView()