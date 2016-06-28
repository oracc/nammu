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

from javax.swing import JTextPane, BorderFactory
from java.awt.event import MouseAdapter

from ..utils import set_font


class AtfEditArea(JTextPane):

    def __init__(self, controller):
        self.controller = controller
        self.border = BorderFactory.createEmptyBorder(4, 4, 4, 4)
        self.font = set_font()
        # If this is not done, no tooltips appear
        self.setToolTipText("")
        # Consume mouse events when over this JTextPane
        listener = CustomMouseListener(self)
        self.addMouseListener(listener)

    def getToolTipText(self, event=None):
        """
        Overrides getToolTipText so that tooltips are only displayed when a
        line contains a validation error.
        """
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
                    return err_msg.decode('utf-8')

    def get_line_num(self, position):
        """
        Returns line number given mouse position in text area.
        """
        text = self.text[0:position]
        return text.count('\n') + 1

    def setText(self, text):
        '''
        Override JTextPane's setText to call syntax highlighting so that it
        still works when you set text from elsewhere in the code.
        '''
        super(AtfEditArea, self).setText(text)
        self.controller.syntax_highlight()
        self.controller.update_line_numbers()

    def cut(self):
        '''
        Override JTextPane's cut to call syntax highlighting so that it still
        works when user cuts text via toolbar button or mouse.
        '''
        super(AtfEditArea, self).cut()
        self.controller.syntax_highlight()
        self.controller.update_line_numbers()

    def copy(self):
        '''
        Override JTextPane's copy to call syntax highlighting so that it still
        works when user copies text via toolbar button or mouse.
        '''
        super(AtfEditArea, self).copy()
        self.controller.syntax_highlight()
        self.controller.update_line_numbers()

    def paste(self):
        '''
        Override JTextPane's paste to call syntax highlighting so that it still
        works when user pastes text via toolbar button or mouse.
        '''
        super(AtfEditArea, self).paste()
        self.controller.syntax_highlight()
        self.controller.update_line_numbers()


class CustomMouseListener(MouseAdapter):
    """
    Consumes mouse events.
    """
    def __init__(self, panel):
        self.panel = panel

    def mousePressed(self, event):
        offset = self.panel.viewToModel(event.getPoint())
