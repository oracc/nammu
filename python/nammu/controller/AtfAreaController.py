'''
Copyright 2015 - 2017 University College London.

This file is part of Nammu.

Nammu is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Nammu is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Nammu.  If not, see <http://www.gnu.org/licenses/>.
'''

from javax.swing.undo import CannotUndoException, CannotRedoException
from java.awt import Color

from ..view.AtfAreaView import AtfAreaView
from ..view.LineNumbersArea import LineNumbersArea
from ..view.AtfEditArea import AtfEditArea
from ..view.SyntaxHighlighter import SyntaxHighlighter
import TextLineNumber
import re


class AtfAreaController(object):
    '''
    Creates the ATF area (edit/object) view and handles its actions.
    '''
    def __init__(self, mainControler):
        # Create text edition area
        self.edit_area = AtfEditArea(self)
        self.secondary_area = AtfEditArea(self)
        # Create text panel to display the line numbers
        self.line_numbers_area = TextLineNumber(self.edit_area)
        self.secondary_line_numbers = TextLineNumber(self.secondary_area)
        # Create view with a reference to its controller to handle events
        self.view = AtfAreaView(self)
        # Will also need delegating to parent presenter
        self.controller = mainControler
        # Get a reference to the view's undo_manager
        self.undo_manager = self.view.undo_manager
        # Initialise validation errors
        self.validation_errors = {}
        # Needed by syntax highlighter
        self.edit_area_styledoc = self.edit_area.getStyledDocument()
        # Synch content of split editor panes
        self.secondary_area.setStyledDocument(
                                            self.edit_area.getStyledDocument())
        # Syntax highlighting
        self.syntax_highlighter = SyntaxHighlighter(self)

    def setAtfAreaText(self, text):
        '''
        Need to manually force an edit compound because the setText() method
        triggers 2 consecutive INSERT events: one to set the text to "" and
        another to set the text to the given text.
        Default behaviour of the compound edit would create a new edit for each
        INSERT event, so we have to manually group those two together.
        '''
        self.view.edit_listener.force_start_compound()
        self.view.edit_area.setText(text)
        self.view.edit_listener.force_stop_compound()

    def getAtfAreaText(self):
        '''
        Short hand for getting Nammu's text area's content.
        '''
        return self.view.edit_area.getText()

    def clearAtfArea(self):
        '''
        Every time we clear the ATF text area we also need to clear the edits
        pile, repaint the line numbers and remove the styling from previous
        validation highlight.
        '''
        self.setAtfAreaText("")
        # When opening a new file we should discard the previous edits
        self.view.undo_manager.discardAllEdits()
        # Clear tooltips
        self.clearToolTips()
        # Clear validation errors
        self.validation_errors = {}

    def clearToolTips(self):
        '''
        We don't want tooltips from previous validations appearing after the
        file has been re-validated or another file has been opened.
        '''
        self.view.edit_area.setToolTipText(None)

    def set_validation_errors(self, validation_errors):
        '''
        Short hand for refreshing validation errors in ATF area.
        '''
        self.validation_errors = validation_errors

    def undo(self):
        '''
        CompoundEdits only get added  to the undo manager when the next
        INSERT/REMOVE event happens. Thus, if we are adding changes to
        the current compound edit and we want to undo it before the next
        INSERT/REMOVE happens, we won't be able until it's been explicitly
        ended.
        '''
        self.view.edit_listener.current_compound.end()
        try:
            self.undo_manager.undo()
        except CannotUndoException:
            # This exception indicates we've reached the end of the edits
            # vector Nothing to do
            pass
        else:
            self.syntax_highlight()

    def redo(self):
        try:
            self.undo_manager.redo()
        except CannotRedoException:
            # This exception indicates we've reached the end of the edits
            # vector - Nothing to do
            pass
        else:
            self.syntax_highlight()

    def __getattr__(self, name):
        '''
        Calls to copy, paste and cut, getSelectedText, getSelectionStart
        methods are just passed to text area. replaceSelection and
        setCaretPosition require the wrapper to handle their args.
        '''
        if name in ('copy', 'paste', 'cut', 'getSelectedText',
                    'getSelectionStart'):
            return getattr(self.edit_area, name)

        elif name in ('replaceSelection', 'setCaretPosition'):

            def wrapper(*args, **kw):
                return getattr(self.edit_area, name)(*args, **kw)
            return wrapper

    def get_viewport_top_bottom(self, top, bottom):
        '''
        Get the top and bottom of the viewport from scroll events
        '''
        top_line = self.edit_area.get_line_num(top)
        bottom_line = self.edit_area.get_line_num(bottom)

        return top_line, bottom_line

    def syntax_highlight(self, top_caret=None, bottom_caret=None):
        '''
        Short hand for syntax highlighting. Takes the line bounds.
        '''
        if top_caret is not None and bottom_caret is not None:
            top_line, bottom_line = self.get_viewport_top_bottom(top_caret,
                                                                 bottom_caret)
            self.syntax_highlighter.syntax_highlight(top_line,
                                                     bottom_line,
                                                     top_caret,
                                                     bottom_caret)
        else:
            self.syntax_highlighter.syntax_highlight()

    def highlight_matches(self, matches, offset, current_match=None):
        self.syntax_highlighter.highlight_matches(matches,
                                                  offset,
                                                  current_match)

    def splitEditor(self, split_orientation):
        '''
        Toggles split editor view.
        '''
        self.view.toggle_split(split_orientation)

    def restore_highlight(self):
        '''
        Turn off syntax highlight of matches.
        '''
        length = len(self.getAtfAreaText())
        self.syntax_highlighter._highlight_match(0, length, Color.white)
        self.syntax_highlighter.syntax_highlight()

    def getPositionFromLine(self, text, line_num):
        '''
        Given a block of text and a line number, return the caret position
        at the start of the given line.
        '''
        if len(text) > 0 and line_num != 1:
            compiled = re.compile(r"\n")
            textiter = compiled.finditer(text)
            pos = [m.start() for m in textiter][line_num - 2]
        else:
            pos = 0

        return pos
