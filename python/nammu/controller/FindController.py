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
        self.ongoing_find_next = False

    def replace_all(self, old_text, new_text, ignore_case, regex, selection):
        '''
        Change all matches in the text with new given text.
        '''
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

    def find_next(self, text, ignore_case, regex, selection):
        '''
        Highlight all matches and place cared/focus on next one.
        '''
        # Check wether there is some text in the text area.
        atf_text = self.atfAreaController.getAtfAreaText()
        offset = 0
        if atf_text:
            # If user chooses to find on selection, check if any text is
            # selected and if so, work only on that selection.
            if selection:
                atf_text = self.atfAreaController.getSelectedText()
                offset = self.atfAreaController.getSelectionStart()

            matches = self._find_matches(atf_text, text, ignore_case, regex,
                                         offset)
            print(matches)
            # Highlight all matches

            # Move focus to first match found

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

    def _find_matches(self, text, expr, ignore_case, regex, offset):
        '''
        Returns a list with the begining position of all matches of a given
        text in the ATF area.
        '''
        matches = []
        if not regex:
            expr = re.escape(expr)
        if ignore_case:
            pattern = re.compile(expr, re.IGNORECASE)
        else:
            pattern = re.compile(expr)
        for match in pattern.finditer(text):
            # Add offset in case of user has selected text
            matches.append(match.start() + offset)
        return matches
