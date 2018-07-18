# -*- coding: utf-8 -*-
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

import logging

from swingutils.events import addEventListener
from java.awt import (Color, BorderLayout, GridBagLayout, GridBagConstraints,
                      Insets)
from javax.swing import (JDialog, JFrame, JPanel, JButton, JCheckBox,
                         JEditorPane, JScrollPane, BorderFactory)
from javax.swing.event import HyperlinkListener
from javax.swing.event.HyperlinkEvent import EventType
from javax.swing.text.html import HTMLEditorKit


class WelcomeView(JDialog):
    def __init__(self, controller):
        self.logger = logging.getLogger('NammuController')
        self.setAlwaysOnTop(False)
        self.controller = controller

    def display(self):
        '''
        Displays window.
        '''
        self.build()
        self.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        self.setResizable(False)
        self.setTitle('Welcome to Nammu')
        self.pack()
        self.setLocationRelativeTo(None)
        self.visible = 1

    def build(self):
        '''
        Adds the welcome panel to the JDialog window.
        '''
        self.setLayout(BorderLayout())
        self.add(self.build_welcome_panel(), BorderLayout.CENTER)

    def build_welcome_panel(self):
        '''
        Construct the welcome panel here.
        '''
        panel = JPanel(GridBagLayout())
        constraints = GridBagConstraints()
        constraints.insets = Insets(10, 10, 10, 10)

        message = ('<html><body>'
                   '<h1>Welcome to Nammu</h1>'
                   '<h2>An editor for the ORACC project<h2>'
                   '<p>'
                   '<a href=\'oracc\'>Click here</a> for help with ORACC.'
                   '</p>'
                   '<p>Learn more about Nammu <a href=\'nammu\'>here</a>.</p>'
                   '</body></html>')

        # Configure a JEditorPane to display HTML for our welcome message
        msg_pane = JEditorPane()
        msg_pane.setEditable(False)
        kit = HTMLEditorKit()
        msg_pane.setEditorKit(kit)
        scrollPane = JScrollPane(msg_pane)

        # This handles the stylesheet applied to the welcome message
        styleSheet = kit.getStyleSheet()
        styleSheet.addRule('body {color:black; font-size: 16 pt; }')
        styleSheet.addRule('h1 {text-align:center; }')
        styleSheet.addRule('h2 {text-align:center; }')

        # Set the JEditorPane background to match the rest of the window
        msg_pane.border = BorderFactory.createEmptyBorder(4, 4, 4, 4)
        msg_pane.background = Color(238, 238, 238)

        # Add the message and the css and to the JEditorPane
        doc = kit.createDefaultDocument()
        msg_pane.setDocument(doc)
        msg_pane.setText(message)

        # Set up a hyperlink listener
        listener = addEventListener(msg_pane, HyperlinkListener,
                                    'hyperlinkUpdate', self.handleEvent)

        # Configure the placement of the JEditorPane
        constraints.gridx = 1
        constraints.gridy = 1
        constraints.fill = GridBagConstraints.BOTH
        constraints.anchor = GridBagConstraints.CENTER

        panel.add(msg_pane, constraints)

        # Build and place the checkbox
        self.checkbox = JCheckBox('Don\'t show this message again.',
                                  selected=False)
        constraints.gridx = 1
        constraints.gridy = 2
        panel.add(self.checkbox, constraints)

        # Build and place the close button
        close_button = JButton('Close', actionPerformed=self.close_action)

        constraints.gridx = 2
        constraints.gridy = 2
        panel.add(close_button, constraints)

        return panel

    def close_action(self, event):

        if self.checkbox.isSelected():
            # Update settings.yaml
            self.controller.update_welcome_flag(False)

        # Close the welcome window
        self.dispose()

    def handleEvent(self, event):
        '''
        A simple event handler for clicked hyperlinks, to direct to the
        documentation and the github repo.
        '''
        if event.getEventType() is EventType.ACTIVATED:

            # Shorthand for NammuController
            nammu = self.controller.controller

            nammu._open_website(nammu.urls[event.getDescription()])
