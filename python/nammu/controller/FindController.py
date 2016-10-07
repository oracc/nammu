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

    def _find_matches(self, expr, regex, ignore_case):
        '''
        Returns a list with the begining position of all matches of a given
        text in the ATF area.
        '''
        text = self.atfAreaController.getAtfAreaText()
        matches = []
        if not regex:
            expr = re.escape(expr)
        if ignore_case:
            pattern = re.compile(expr, re.IGNORECASE)
        else:
            pattern = re.compile(expr)
        for match in pattern.finditer(text):
            matches.append(match.start())
        return matches
