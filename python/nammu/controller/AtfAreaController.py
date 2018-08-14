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
from javax.swing import JTextPane
from java.awt import Color

from ..view.AtfAreaView import AtfAreaView
from ..view.AtfEditArea import AtfEditArea
from ..view.SyntaxHighlighter import SyntaxHighlighter
import TextLineNumber
import re

from ..utils import set_font


class AtfAreaController(object):
    '''
    Creates the ATF area (edit/object) view and handles its actions.
    '''
    def __init__(self, mainControler):
        # Will also need delegating to parent presenter
        self.controller = mainControler
        # Create text edition area
        self.edit_area = AtfEditArea(self)
        self.caret = self.edit_area.getCaret()
        self.secondary_area = AtfEditArea(self)
        self.arabic_area = JTextPane()

        # Create text panel to display the line numbers
        self.line_numbers_area = TextLineNumber(self.edit_area)
        self.secondary_line_numbers = TextLineNumber(self.secondary_area)
        self.arabic_line_numbers = TextLineNumber(self.arabic_area)
        # Ensure the line numbers update when the editor font is changed
        self.line_numbers_area.setUpdateFont(True)
        self.secondary_line_numbers.setUpdateFont(True)
        self.arabic_line_numbers.setUpdateFont(True)
        # Create view with a reference to its controller to handle events
        self.view = AtfAreaView(self)
        # Get a reference to the view's undo_manager
        self.undo_manager = self.view.undo_manager
        # Initialise validation errors
        self.validation_errors = {}
        # Needed by syntax highlighter
        self.edit_area_styledoc = self.edit_area.getStyledDocument()
        # Synch content of split editor panes
        self.secondary_area.setStyledDocument(
                                            self.edit_area.getStyledDocument())
        # Temporary fix for arabic translation area
        # self.arabic_area.setText("")

        # Syntax highlighting
        self.syntax_highlighter = SyntaxHighlighter(self)

        # Set the arabic area's font size to match the user difened value
        # Setting the edit area here as well forces both line numbers to be
        # the same size
        self.conf = self.controller.config
        font = set_font(self.conf['edit_area_style']['fontsize']['user'])
        self.arabic_area.setFont(font)
        self.edit_area.setFont(font)
        self.secondary_area.setFont(font)

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

    def clearAtfArea(self, arabic=False):
        '''
        Every time we clear the ATF text area we also need to clear the edits
        pile, repaint the line numbers and remove the styling from previous
        validation highlight.
        '''
        self.setAtfAreaText("")
        if arabic:
            self.arabic_area.setText("")
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

    def pad_top_viewport_caret(self, top_left_char, text):
        '''
        Extend the top of the viewport to the nearest header, so we don't
        have problems with malformed atf files being highlighted.
        '''

        # Test that there is text in the edit area
        if len(text) == 0:
            return top_left_char

        # Test if the line we are currently on is a header line
        if text[top_left_char] == '&':
            return top_left_char

        # slice text to only contain the characters above the viewport
        text_above = text[:top_left_char]
        # This catches malformed headers at the top of a file.
        if len(text_above) == 0:
            return top_left_char

        # Split the text above the viewport into lines
        lines = text_above.split('\n')
        header_line_no = None

        # Iterate over the list backwards, as this is more efficient
        for line_no, line in reversed(list(enumerate(lines))):
            if line.startswith('&'):
                header_line_no = line_no
                break

        # line 0 will evaluate as false so need to be explicit here
        if header_line_no is not None:
            # If we have a header line, in the text above the viewport,
            # update the top_left_char value
            cursor_line_no = self.edit_area.get_line_num(top_left_char)
            char_count = len('\n'.join(lines[header_line_no:cursor_line_no]))

            top_left_char -= char_count

            # This will catch any errors if the char_count goes wrong
            if top_left_char < 0:
                top_left_char = 0

            return top_left_char
        else:
            return top_left_char

    def pad_bottom_viewport_caret(self, bottom_left_char, text):
        '''
        Adds two lines to the bottom of the viewport so we dont have any
        unhighlighted lines visible.
        '''

        # Test that there is text in the edit area
        if len(text) == 0:
            return bottom_left_char

        # slice text to only contain the characters below the viewport
        text_below = text[bottom_left_char:]

        # Check there is text below the viewport
        if len(text_below) == 0:
            return bottom_left_char

        # Split the text below the viewport into lines
        lines = text_below.split('\n')

        # Get no of chars on the last line of the viewport and the next 2 lines
        char_count = len('\n'.join(lines[:3]))
        bottom_left_char += char_count

        return bottom_left_char

    def update_error_lines(self, caret_line, no_of_lines, flag):
        '''
        Given a caret line number, a number of lines and a flag indicating
        whether the error lines need incremented ('insert') or decremented
        ('remove'). Update the line numbers of the keys in the dictionary
        self.validation_errors so that error highlighting follows broken lines
        during editing.
        '''

        # If the supplied edit does not add or remove any lines, do nothing
        if no_of_lines < 1:
            return

        error_lines = self.validation_errors.keys()

        # For legacy reasons the keys are strings, but we need ints
        e_lines_int = [int(a) for a in error_lines]

        # We only care about edits hapenning above error lines
        if caret_line > max(e_lines_int):
            return

        # We need the line end position and the caret position
        positions = self.getLinePositions(self.view.oldtext)
        caret_pos = self.edit_area.getCaretPosition()
        line_end = positions[caret_line - 1][1]

        tmp = {}
        for q, err in enumerate(e_lines_int):
            # We are above an error line or on an error line but not at its end
            if (err > caret_line) or (err == caret_line and
                                      caret_pos != line_end):
                fixed_line_no = self.line_fix(e_lines_int[q], no_of_lines,
                                              flag)

                # rebuild self.controller.validation_errors
                tmp[str(fixed_line_no)] = self.validation_errors[str(err)]

            # We are below or after the error lines so do nothing
            else:
                tmp[str(err)] = self.validation_errors[str(err)]

        # Write the updated line numbers to the error dictionary
        self.validation_errors = tmp

    def line_fix(self, e_line_no, no_of_lines, flag):
        '''
        Helper function containing the logic for incrementing or decrementing
        line numbers
        '''
        if flag == 'insert':
            e_line_no += no_of_lines
        elif flag == 'remove':
            e_line_no -= no_of_lines
            # handle potential out of bounds - 1 is top of the file
            if e_line_no < 1:
                e_line_no = 1

        return e_line_no

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

    def splitEditorArabic(self, split_orientation, atf_body, atf_translation):
        '''
        Toggles split editor view.
        '''
        self.view.toggle_split_arabic(split_orientation,
                                      atf_body,
                                      atf_translation)

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

    def getLinePositions(self, text):
        '''
        Given a block of text, return the caret positions
        at the start and end of each line as a list of tuples in the order
        (start, end) assuming left to right text.
        The hacky list addition is to handle off by one errors as the 1st line
        starts at position 0, whereas every other line starts at +1 past the
        end of the last line and we also need to add in the final line length
        manually.
        '''
        if len(text) > 0:
            compiled = re.compile(r"\n")
            textiter = compiled.finditer(text)
            pos = [m.start() for m in textiter]
        else:
            return [(0, 0)]

        # Build lists of the starts and ends of each line
        starts = [0] + [x + 1 for x in pos]
        ends = pos + [len(text)]

        return zip(starts, ends)

    def refreshEditArea(self):
        '''
        Repaint edit area with appeareance chosen by user.
        '''
        self.view.refresh()

    def findArabic(self, text):
        '''
        Returns the caret position of the beginning of the arabic block, if one
        is found. Otherwise returns None.

        Add additional values to lang_codes or trans_types if we need to
        support other translation styles or right to left langages in the
        future
        '''
        lang_codes = '|'.join(['ar', 'fa', 'ku'])
        trans_types = '|'.join(['parallel', 'labeled', 'unitary'])

        regex = r'@translation(\s({}))(\s({})\s)(.*\n)+?'.format(trans_types,
                                                                 lang_codes)
        comp = re.compile(regex)
        search = comp.search(text, re.MULTILINE)
        if search:
            return search.start()
        else:
            return None

    def concatenate_arabic_text(self):
        '''
        Convienience method to get the text from the main text pane and the
        arabic pane and join them together so files can be saved properly.
        '''
        return u'{}{}'.format(self.edit_area.getText(),
                                self.arabic_area.getText())
