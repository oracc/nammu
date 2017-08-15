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
import os
from swingutils.events import addEventListener

from java.awt import GridLayout, Component, FlowLayout, Color, BorderLayout
from java.awt import GridBagLayout, GridBagConstraints, Insets
from javax.swing import JDialog, JFrame, JTabbedPane, JComponent, JPanel
from javax.swing import JLabel, BoxLayout, JTextField, JButton, JCheckBox
from javax.swing import JFileChooser, JEditorPane
from javax.swing.border import EmptyBorder
from javax.swing.event import HyperlinkListener
from javax.swing.event.HyperlinkEvent import EventType


class WelcomeView(JDialog):
    def __init__(self, controller):
        self.logger = logging.getLogger('NammuController')
        self.setAlwaysOnTop(False)
        self.controller = controller
        self.new_user = self.controller.config['new_user']
        self.pane = self.getContentPane()  # Not sure about this.

    def display(self):
        '''
        Displays window.
        '''
        self.build()
        self.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        self.setResizable(False)
        self.setTitle('Welcome to Nammu')
        self.pack()  # What does this do?
        self.setLocationRelativeTo(None)
        self.visible = 1

    def build(self):
        '''
        Create all tab panels and put together to form the settings window.
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

        doc_button = JButton('Documentation', actionPerformed=self.mock_action)
        panel.add(doc_button, constraints)

        nammu_button = JButton('About Nammu', actionPerformed=self.mock_action)
        panel.add(nammu_button, constraints)

        close_button = JButton('Close', actionPerformed=self.close_action)
        panel.add(close_button, constraints)

        message = ('<html>Welcome to Nammu, an editor for the ORACC project'
                  '<a href=\'oracc\'>Click here</a> for help getting started '
                  ' with ORACC and <a href=\'nammu\'>here</a> to learn more'
                  ' about Nammu</html>')
        welcome_label = JEditorPane('text/html', message)

        # Disable writing in the console - required to render hyperlinks
        welcome_label.setEditable(False)

        # Set up a hyperlink listener
        listener = addEventListener(welcome_label, HyperlinkListener,
                                    'hyperlinkUpdate', self.handleEvent)

        panel.add(welcome_label, constraints)

        self.checkbox = JCheckBox('Don\'t show this message again.', selected=False)
        panel.add(self.checkbox, constraints)

        return panel

    def mock_action(self, event):
        print 'Hello world'

    def close_action(self, event):

        if self.checkbox.isSelected():
            # Update settings.yaml
            self.controller.update_welcome_flag(False)

        # Close the welcome window
        self.dispose()


    def handleEvent(self, event):
        '''
        A simple event handler for clicked hyperlinks, to direct to the
        documentation and the github repo
        '''
        if event.getEventType() is EventType.ACTIVATED:

            urls = {'nammu': 'https://github.com/oracc/nammu',
                    'oracc': ('http://oracc.museum.upenn.edu/doc/help/'
                              'editinginatf/')}

            clicked = event.getDescription()

            self.controller.controller._open_website(urls[clicked])
