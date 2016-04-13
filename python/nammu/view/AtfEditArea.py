from java.awt import Font
from javax.swing import JTextPane, BorderFactory
from java.awt.event import MouseAdapter


class AtfEditArea(JTextPane):
    def __init__(self):
        self.border = BorderFactory.createEmptyBorder(4, 4, 4, 4)
        self.font = Font("Monaco", Font.PLAIN, 14)
        # Tooltip
        self.setToolTipText("Hello")

        listener = CustomMouseListener(self)
        self.addMouseListener(listener)

class CustomMouseListener(MouseAdapter):
    def __init__(self, panel):
        self.panel = panel
    def mousePressed(self, event):
        offset = self.panel.viewToModel(event.getPoint())
        print offset
