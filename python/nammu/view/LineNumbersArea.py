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

from java.awt import Color
from javax.swing import JTextPane, BorderFactory
from javax.swing.text import SimpleAttributeSet, StyleConstants, DefaultCaret

from ..utils import set_font


class LineNumbersArea(JTextPane):
    def __init__(self):
        """
        Line numbers need to be displayed in a separate panel with different
        styling.
        """
        # Align right
        para_attribs = SimpleAttributeSet()
        StyleConstants.setAlignment(para_attribs, StyleConstants.ALIGN_RIGHT)
        self.setParagraphAttributes(para_attribs, True)

        # Use default font style
        default_attribs = SimpleAttributeSet()
        self.font = set_font()
        StyleConstants.setFontFamily(default_attribs, self.font.getFamily())
        StyleConstants.setFontSize(default_attribs, self.font.getSize())
        StyleConstants.setForeground(default_attribs, Color.gray)
        self.setCharacterAttributes(default_attribs, True)

        # Initialize content
        border = BorderFactory.createEmptyBorder(4, 4, 4, 4)
        self.border = border
        self.setText("1: \n")
        self.setEditable(False)

        # Prevent auto scroll down when line numbers are repainted
        caret = self.getCaret()
        caret.setUpdatePolicy(DefaultCaret.NEVER_UPDATE)
