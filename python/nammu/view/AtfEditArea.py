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

import re
from swingutils.threads.swing import runSwingLater

from javax.swing import JTextPane, BorderFactory
from java.awt.event import MouseAdapter

import MyStyledEditorKit


class AtfEditArea(JTextPane):

    def __init__(self, controller):
        # This custom StyledEditorKit fixes broken line wrapping.
        self.setEditorKit(MyStyledEditorKit())
        self.controller = controller
        self.border = BorderFactory.createEmptyBorder(4, 4, 4, 4)
        # If this is not done, no tooltips appear
        self.setToolTipText("")
        # Consume mouse events when over this JTextPane
        listener = CustomMouseListener(self)
        self.addMouseListener(listener)

    def getToolTipText(self, event=None):
        '''
        Overrides getToolTipText so that tooltips are only displayed when a
        line contains a validation error.
        '''
        if event:
            position = self.viewToModel(event.getPoint())
            line_num = str(self.get_line_num(position))
            # Check if line_num has an error message assigned
            if self.controller.validation_errors:
                try:
                    err_msg = self.controller.validation_errors[line_num]
                except KeyError:
                    # Current line has no error messages assigned
                    # Returning None also switches off tooltips from previous
                    # validation errors.
                    return None
                else:
                    # Use this regex to strip the hyperlink tags before
                    # displaying the tooltip
                    err_msg = re.sub('<.+?>', '', err_msg)
                    return err_msg.decode('utf-8')

    def get_line_num(self, position):
        '''
        Returns line number given mouse position in text area.
        '''
        text = self.text[0:position]
        return text.count('\n') + 1

    def setText(self, text):
        '''
        Override JTextPane's setText to call syntax highlighting so that it
        still works when you set text from elsewhere in the code.
        '''
        super(AtfEditArea, self).setText(text)

        # Deploy syntax highlighting in a new thread
        runSwingLater(self.controller.controller.initHighlighting)

    def replaceSelection(self, text):
        '''
        Override JTextPane's replaceSelection to call syntax highlighting
        after replacing some text.
        '''
        super(AtfEditArea, self).replaceSelection(text)

    def cut(self):
        '''
        Override JTextPane's cut to call syntax highlighting so that it still
        works when user cuts text via toolbar button or mouse.
        '''
        super(AtfEditArea, self).cut()

    def copy(self):
        '''
        Override JTextPane's copy to call syntax highlighting so that it still
        works when user copies text via toolbar button or mouse.
        '''
        super(AtfEditArea, self).copy()

    def paste(self):
        '''
        Override JTextPane's paste to call syntax highlighting so that it still
        works when user pastes text via toolbar button or mouse.
        '''
        super(AtfEditArea, self).paste()


class CustomMouseListener(MouseAdapter):
    '''
    Consumes mouse events.
    '''
    def __init__(self, panel):
        self.panel = panel

    def mousePressed(self, event):
        offset = self.panel.viewToModel(event.getPoint())
