'''
Created on 15 Apr 2015

Creates the ATF area (edit/object) view and handles its actions.

@author: raquel-ucl
'''

from javax.swing.undo import CannotUndoException, CannotRedoException
from ..view.AtfAreaView import AtfAreaView


class AtfAreaController(object):

    def __init__(self, mainControler):
        # Create view with a reference to its controller to handle events
        self.view = AtfAreaView(self)

        # Will also need delegating to parent presenter
        self.controller = mainControler

        # Get a reference to the view's undo_manager
        self.undo_manager = self.view.undo_manager

    def setAtfAreaText(self, text):
        self.view.editArea.setText(text)
        self.view.syntax_highlight()
        self.update_line_numbers()


    def getAtfAreaText(self):
        return self.view.editArea.getText()


    def clearAtfArea(self):
        self.view.editArea.setText("")
        self.view.undo_manager.discardAllEdits()


    def update_line_numbers(self):
        # Get how many lines are in the file
        n_lines = self.getAtfAreaText().count('\n')

        # Reload line numbers text panel
        self.view.repaint_line_numbers(n_lines)


    def undo(self):
        print self.undo_manager.toString()
        try:
            self.undo_manager.undo()
        except CannotUndoException:
            pass


    def redo(self):
        print self.undo_manager.toString()
        try:
            self.undo_manager.redo()
        except CannotRedoException:
            pass
