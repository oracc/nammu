'''
Created on 15 Apr 2015

Creates the ATF area (edit/object) view and handles its actions.

@author: raquel-ucl
'''

from ..view.AtfAreaView import AtfAreaView

class AtfAreaController():
    
    def __init__(self, mainControler):
        print "I'm the ATF area controller"
        
        #Create view with a reference to its controller to handle events
        self.view = AtfAreaView(self)
        
        #Will also need delegating to parent presenter
        self.controller = mainControler
        
    def setAtfAreaText(self, text):
        self.view.editArea.setText(text)
        
        