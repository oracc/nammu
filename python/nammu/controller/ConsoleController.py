'''
Created on 15 Apr 2015

Creates the console view and handles console actions.

@author: raquel-ucl
'''

from ..view.ConsoleView import ConsoleView

class ConsoleController(object):

    def __init__(self, mainControler):
        # Create view with a reference to its controller to handle events
        self.view = ConsoleView(self)
        # Will also need delegating to parent presenter
        self.controller = mainControler

    def addText(self, text):
        self.view.editArea.append(text)
        self.view.scroll()
