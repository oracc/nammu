'''
Created on 15 Apr 2015

Creates the menu view and handles menu actions.

@author: raquel-ucl
'''

from ..view.MenuView import MenuView

class MenuController():
    
    def __init__(self, mainController):
        
        #Create view with a reference to its controller to handle events
        self.view = MenuView(self)
        
        #Will also need delegating to parent presenter
        self.controller = mainController
        
    #Some actions need to be delegated to NammuController.
    #E.g. actions in menu that'll need modification of text area controlled 
    #elsewhere and not accessible from this controller; as opposed to e.g. 
    #showHelp that can be dealt with from MenuController.

    #Whenever a MenuController's method is invoked, __getattr__ will search for 
    #that given method name in this class. If it's not found, it'll delegate the
    #action with same name to NammuController
    def __getattr__(self, name):
        return getattr(self.controller, name)
       
    def validate(self, atfFile):
        self.controller.validate(atfFile)
        
    def lemmatise(self, atfFile):
        self.controller.lemmatise(atfFile)
        
    def showHelp(self):
        """ 
        1. Show popup window with help (or just open firefox with ORACC info?)
        """
        
    def showAbout(self):
        """ 
        1. Show popup window with help (or just open firefox with ORACC info?)
        """
        
