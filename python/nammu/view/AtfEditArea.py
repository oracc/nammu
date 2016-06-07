from javax.swing import JTextPane, BorderFactory
from java.awt.event import MouseAdapter

from ..utils import set_font


class AtfEditArea(JTextPane):

    def __init__(self, parent_component):
        self.parent_component = parent_component
        self.border = BorderFactory.createEmptyBorder(4, 4, 4, 4)
        self.font = set_font('DejaVuSans')
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
            if self.parent_component.validation_errors:
                try:
                    err_msg = self.parent_component.validation_errors[line_num]
                except KeyError:
                    # Current line has no error messages assigned
                    pass
                else:
                    return err_msg

    def get_line_num(self, position):
        """
        Returns line number given mouse position in text area.
        """
        text = self.text[0:position]
        return text.count('\n') + 1


class CustomMouseListener(MouseAdapter):
    """
    Consumes mouse events.
    """
    def __init__(self, panel):
        self.panel = panel

    def mousePressed(self, event):
        offset = self.panel.viewToModel(event.getPoint())
