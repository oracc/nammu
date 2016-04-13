from java.awt import Font
from javax.swing import JTextPane, BorderFactory


class AtfEditArea(JTextPane):
    def __init__(self):
        self.border = BorderFactory.createEmptyBorder(4, 4, 4, 4)
        self.font = Font("Monaco", Font.PLAIN, 14)
        # Tooltip
        self.setToolTipText("Hello")
