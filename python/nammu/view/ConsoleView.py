'''
Copyright 2015 - 2018 University College London.

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

from swingutils.events import addEventListener

from java.awt import BorderLayout, Color, Dimension
from javax.swing import JEditorPane, JScrollPane, JPanel, BorderFactory
from javax.swing.text import DefaultCaret
from javax.swing.event import HyperlinkListener
from javax.swing.event.HyperlinkEvent import EventType


class ConsoleView(JPanel):
    '''
    Initializes the console view and sets its layout.
    '''
    def __init__(self, controller):
        '''
        Creates default empty console-looking panel.
        It should be separated from the rest of the GUI so that users can
        choose to show or hide the console. Or should it be a split panel?
        This panel will display log and validation/lemmatization messages.
        It might need its own toolbar for searching, etc.
        It will also accept commands in later stages of development, if need
        be.
        '''
        # Give reference to controller to delegate action response
        self.controller = controller

        # Make text area occupy all available space and resize with parent
        # window
        self.setLayout(BorderLayout())

        # Create console-looking area
        self.edit_area = JEditorPane()

        # Although most of the styling is done using css, we need to set these
        # properties to ensure the html is rendered properly in the console
        self.edit_area.border = BorderFactory.createEmptyBorder(6, 6, 6, 6)
        self.edit_area.setContentType("text/html")

        # Disable writing in the console - required to render hyperlinks
        self.edit_area.setEditable(False)

        # Map CSS color strings to Java Color objects
        self.colors = {'Gray': Color(238, 238, 238),
                       'Black': Color(0, 0, 0),
                       'Yellow': Color(255, 255, 0)}

        # Initial call to refresh console to set the console style properties
        self.refreshConsole()

        # Set up a hyperlink listener
        listener = addEventListener(self.edit_area, HyperlinkListener,
                                    'hyperlinkUpdate', self.handleEvent)

        # Will need scrolling controls
        scrollingText = JScrollPane(self.edit_area)
        scrollingText.setPreferredSize(Dimension(1, 150))

        # Make text area auto scroll down to last printed line
        caret = self.edit_area.getCaret()
        caret.setUpdatePolicy(DefaultCaret.ALWAYS_UPDATE)

        # Add to parent panel
        self.add(scrollingText, BorderLayout.CENTER)

    def refreshConsole(self):
        '''
        Restyle console using CSS with user selected appearance settings.
        '''
        fontsize = self.controller.config['console_style']['fontsize']['user']
        background_color = self.controller.config[
                                'console_style']['background_color']['user']
        font_color = self.controller.config[
                                'console_style']['font_color']['user']

        bodyRule = ("body {{ font-family: Monaco; font-size: {0} pt; "
                    "font-weight: bold; color: {1} }}").format(fontsize,
                                                               font_color)
        # Set font properties
        doc = self.edit_area.getDocument()
        doc.getStyleSheet().addRule(bodyRule)

        # Set background color
        self.edit_area.background = self.colors[background_color]
        self.edit_area.repaint()

    def scroll(self):
        '''
        Scroll down to bottom.
        '''
        length = self.edit_area.getDocument().getLength()
        self.edit_area.setCaretPosition(length)

    def handleEvent(self, event):
        '''
        A simple event handler for clicked hyperlinks.
        '''
        if event.getEventType() is EventType.ACTIVATED:

            atfCont = self.controller.controller.atfAreaController

            error_line = int(event.getDescription())
            text = atfCont.getAtfAreaText()
            pos = atfCont.getPositionFromLine(text, error_line)

            # pos gives the position of the final character on the previous
            # line, so add 1 char to move the caret to the start of error_line
            # The method is called twice to catch the edge case where the user
            # has the caret in the correct location prior to the click
            # resulting in the screen not scrolling to the error line.
            # This would be done with some logic around getCaretPosition(), but
            # this would need a caret listener to be constructed.
            for i in xrange(2):
                atfCont.setCaretPosition(pos + i)

            # Return focus to the editor window
            atfCont.edit_area.requestFocusInWindow()
