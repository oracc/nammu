'''
Copyright 2015, 2016 University College London.

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

import re
from ..view.FindView import FindView
from javax.swing.text import BadLocationException


class FindController(object):
    def __init__(self, maincontroller):
        self.controller = maincontroller
        self.atfAreaController = self.controller.atfAreaController
        self.view = FindView(self)
        self.view.display()
        self.matches = None
        self.expr = None
        self.offset = 0
        self.ignore_case = False
        self.regex = False
        self.selection = False
        self.selected_text = None

    def replace_all(self, old_text, new_text, ignore_case, regex, selection):
        '''
        Change all matches in the text with new given text.
        '''
        self.expr = new_text
        self.ignore_case = ignore_case
        self.regex = regex
        self.selection = selection
        # Check wether there is some text in the text area.
        current = self.atfAreaController.getAtfAreaText()
        if current:
            # If user chooses to replace on selection, check if any text is
            # selected and if so, work only on that selection.
            if selection:
                selected = self.atfAreaController.getSelectedText()
                if selected:
                    replaced = self._replace_all_in_text(selected, old_text,
                                                         new_text, ignore_case,
                                                         regex)
                    self.atfAreaController.replaceSelection(replaced)
            else:
                replaced = self._replace_all_in_text(current, old_text,
                                                     new_text, ignore_case,
                                                     regex)
                self.atfAreaController.setAtfAreaText(replaced)

    def find_next(self, expr, ignore_case, regex, selection):
        '''
        Highlight all matches and place caret/focus on next one.
        '''
        # Check if this is the first time find is used for this given text
        self.reset = False
        if self.ignore_case != ignore_case:
            self.ignore_case = ignore_case
            self.reset = True
        if self.regex != regex:
            self.regex = regex
            self.reset = True
        if self.selection != selection:
            self.selection = selection
            self.reset = True
        if self.expr != expr:
            self.expr = expr
            self.reset = True
        if self.reset:
            # TODO:Forget about previous text selections?
            # self.selected_text = None
            self.matches = self._find_all_matches()
            if self.matches:
                # Highlight all matches, taking selection offset into account
                self.controller.atfAreaController.highlight_matches(
                                                                self.matches,
                                                                self.offset)
                # Move focus to first match found
                # Requires recreating the iterator, though, because it was
                # consumed in the highlighting...
                self.matches = self._find_all_matches()
        try:
            position = self.matches.next().start() + self.offset
            self.controller.atfAreaController.setCaretPosition(position)
        except StopIteration:
            # TODO: If we've reached the last element of the matches list,
            # display message to user. For now just restart to begining of
            # list.
            self.matches = self._find_all_matches()
            try:
                position = self.matches.next().start() + self.offset
                self.controller.atfAreaController.setCaretPosition(position)
            except StopIteration:
                self.matches = self._find_all_matches()
        except AttributeError:
            # TODO: Display window say no matches found
            pass

    def replace_one(self, old_text, new_text, ignore_case, regex, selection):
        '''
        Replace one match and reset the matches in the iterator since
        all the positions will be dependent on the shift caused by the replace.
        Best for now is to find all matches with an offset up to the replaced
        word.
        '''
        # Get current caret position, which will be pointing to the beginning
        # of the word that needs changing.
        caret_position = self.atfAreaController.edit_area.getCaretPosition()
        old_length = len(old_text)
        new_length = len(new_text)
        doc = self.atfAreaController.edit_area_styledoc
        try:
            doc.remove(caret_position, old_length)
            doc.insertString(caret_position, new_text, None)
            # Move caret to next match and highlight matches
            # self.offset = caret_position
        except BadLocationException:
            # We've reached end of text
            # self.offset = 0
            # If length is equal, no need to find all again.
            if old_length != new_length:
                # TODO: find all again, treat as selection starting on
                # caret_position + len(old_text)
                self.matches = self._find_all_matches()
        # If length is equal, no need to find all again.
        if old_length != new_length:
            # TODO: find all again, treat as selection starting on
            # caret_position + len(old_text)
            self.offset = caret_position
            self.matches = self._find_all_matches()
        # In any case, try to find next
        self.find_next(old_text, ignore_case, regex, selection)


    def _find_all_matches(self):
        '''
        Helper method that finds all matches depending on user options.
        '''
        # Check wether there is some text in the text area.
        atf_text = self.atfAreaController.getAtfAreaText()
        if atf_text:
            # If user chooses to find on selection, check if any text is
            # selected and if so, work only on that selection.
            # Note selection will be disabled when caret is moved, so once
            # we reach the end of the selection, the next time getSelectedText
            # will return None. We need to make the selection persistent until
            # next reset.
            if self.selection:
                atf_text = self.atfAreaController.getSelectedText()
                if atf_text:
                    self.selected_text = atf_text
                    self.offset = self.atfAreaController.getSelectionStart()
                elif self.selected_text:
                    atf_text = self.selected_text
                else:
                    self.selected_text = None
                    self.offset = 0
            else:
                self.offset = 0
                self.selected_text = None
            if atf_text:
                return self._find_matches(atf_text)
            else:
                return None

    def _replace_all_in_text(self, atf_text, old_text, new_text, ignore_case,
                             regex):
        '''
        Checks all flags and returns a text after replacing old_text with
        new_text.
        '''
        if not regex:
            old_text = re.escape(old_text)
        if ignore_case:
            pattern = re.compile(old_text, re.IGNORECASE)
            text = pattern.sub(new_text, atf_text)
        else:
            text = re.sub(old_text, new_text, atf_text)
        return text

    def _find_matches(self, text):
        '''
        Returns a list with the begining position of all matches of a given
        text in the ATF area.
        '''
        matches = []
        if not self.regex:
            expr = re.escape(self.expr)
        else:
            expr = self.expr
        if self.ignore_case:
            pattern = re.compile(expr, re.IGNORECASE)
        else:
            pattern = re.compile(expr)
        return pattern.finditer(text)
