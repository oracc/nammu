from java.awt import Color
from javax.swing import JTextPane, BorderFactory
from javax.swing.text import SimpleAttributeSet, StyleConstants


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
        StyleConstants.setFontFamily(default_attribs, "Monaco")
        StyleConstants.setFontSize(default_attribs, 14)
        StyleConstants.setForeground(default_attribs, Color.gray)
        self.setCharacterAttributes(default_attribs, True)

        # Initialize content
        border = BorderFactory.createEmptyBorder(4, 4, 4, 4)
        self.border = border
        self.setText("1: \n")
        self.setEditable(False)
