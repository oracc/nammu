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
        '''
        Need to manually make the edit compound start because the setText()
        method triggers 2 consecutive INSERT events: one to set the text to "" 
        and another to set the text to the given text.
        Default behaviour of the compound edit would create a new edit for each
        INSERT event, so we have to manually group those two together.
        '''
        self.view.edit_listener.compound()
        self.view.editArea.setText(text)
        self.view.syntax_highlight()
        self.view.edit_listener.stop_compound()
        self.update_line_numbers()


    def getAtfAreaText(self):
        return self.view.editArea.getText()


    def clearAtfArea(self):
        self.view.editArea.setText("")
        # When opening a new file we should discard the previous edits
        self.view.undo_manager.discardAllEdits()


    def update_line_numbers(self):
        # Get how many lines are in the file
        n_lines = self.getAtfAreaText().count('\n')
        # Reload line numbers text panel
        self.view.repaint_line_numbers(n_lines)


    def undo(self):
        try:
            # CompoundEdits only get added  to the undo manager when the next 
            # INSERT/REMOVE event happens. Thus, if we are adding changes to
            # the current compound edit and we want to undo it before the next
            # INSERT/REMOVE happens, we won't be able until it's been explicitly 
            # ended.
            self.view.edit_listener.current_compound.end()
            self.undo_manager.undo()
            self.update_line_numbers()
        except CannotUndoException:
            # This exception indicates we've reached the end of the edits vector
            pass


    def redo(self):
        try:
            self.undo_manager.redo()
            self.update_line_numbers()
        except CannotRedoException:
            # This exception indicates we've reached the end of the edits vector
            pass


    def copy(self):
        self.view.editArea.copy()
        
    
    def paste(self):
        self.view.editArea.paste()
        
    
    def cut(self):
        self.view.editArea.cut()