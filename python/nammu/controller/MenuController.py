'''
Created on 15 Apr 2015

Creates the menu view and handles menu actions.

@author: raquel-ucl
'''

from java.lang import System

from ..view.MenuView import MenuView

class MenuController():
    
    def __init__(self, mainPresenter):
        print "I'm the menu controller"
        
        #Create view with a reference to its controller to handle events
        self.view = MenuView(self)
        
        #Will also need delegating to parent presenter
        self.presenter = mainPresenter
        
    #Actions delegated from view. Some of them will need delegation to app
    #controller (eg. action in menu will need modification of text area 
    #controlled elsewhere and not accessible from this controller; eg. quit 
    #Nammu or show help pop up can be dealt with from here)

    def newFile(self):
        print "Creating new file from controller"
        
    def openFile(self):
        print "Opening file from controller"
       
    def saveFile(self):
        print "Saving file from controller"
         
    def closeFile(self):
        print "Closing file from controller"
    
    def quit(self):
        print "Exiting from controller"
        System.exit(0)
        
    def undo(self):
        print "Undoing from controller"
        
    def redo(self):
        print "Redoing from controller"
        
    def copy(self):
        print "Copying from controller"
        
    def cut(self):
        print "Cutting from controller"
        
    def paste(self):
        print "Pasting from controller"
        
    def validate(self, atfFile):
        print "Validating from controller"
        
    def lemmatise(self, atfFile):
        print "Lemmatising from controller"
        
    def showHelp(self):
        print "Showing help popup from controller"
        
    def showAbout(self):
        print "Showing Nammu's info from controller"
        
    def displayModelView(self):
        print "Displaying model view from controller"
        