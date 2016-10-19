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
        Highlight all matches and place cared/focus on next one.
        '''
        # Check if this is the first time find is used for this given text
        reset = False
        if self.ignore_case != ignore_case:
            self.ignore_case = ignore_case
            reset = True
        if self.regex != regex:
            self.regex = regex
            reset = True
        if self.selection != selection:
            self.selection = selection
            reset = True
        if self.expr != expr:
            self.expr = expr
            reset = True
        if reset:
            self.matches = self._find_all_matches()
            # print(self.matches.next().start() + self.offset)
            # Highlight all matches
            # self.controller.atfAreaController.highlight_matches(
                                                            # list(self.matches),
                                                            # len(self.expr))
            self.controller.atfAreaController.highlight_matches(self.matches)
            # TODO: Move focus to first match found
        else:
            # Highlight is already done and matches found, just move cursor
            # to next match
            try:
                # self.view.focus_next_match(self._next_match())
                print(self.matches.next().start() + self.offset)
            except StopIteration:
                # TODO: If we've reached the last element of the matches list,
                # display message to user. For now just restart to begining of
                # list.
                self.matches = self._find_all_matches()
                # self.view.focus_next_match(self._next_match())
                print(self.matches.next().start() + self.offset)

    def _find_all_matches(self):
        '''
        Helper method that finds all matches depending on user options.
        '''
        # Check wether there is some text in the text area.
        atf_text = self.atfAreaController.getAtfAreaText()
        self.offset = 0
        if atf_text:
            # If user chooses to find on selection, check if any text is
            # selected and if so, work only on that selection.
            if self.selection:
                atf_text = self.atfAreaController.getSelectedText()
                self.offset = self.atfAreaController.getSelectionStart()

            matches = self._find_matches(atf_text)
            return matches

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
