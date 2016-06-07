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
        self.font = set_font('DejaVuSans')
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
