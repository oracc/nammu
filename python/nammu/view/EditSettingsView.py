# -*- coding: utf-8 -*-
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

import logging
from java.awt import GridLayout
from javax.swing import JDialog, JFrame, JTabbedPane, JComponent, JPanel
from javax.swing import JLabel


class EditSettingsView(JDialog):
    def __init__(self, controller, config):
        self.logger = logging.getLogger("NammuController")
        self.setAlwaysOnTop(True)
        self.controller = controller
        self.pane = self.getContentPane()
        self.config = config

    def build(self):
        '''
        Put all panels together and form the settings window.
        '''
        self.setLayout(GridLayout(1, 1))
        tabbedPane = JTabbedPane()
        tab_titles = ["General", "Keystrokes", "Languages", "Projects"]
        for title in tab_titles:
            tabbedPane.addTab(title, self.build_settings_pane(title))
        self.add(tabbedPane)

    def build_settings_pane(self, text):
        '''
        Builds empty tab pane.
        '''
        panel = JPanel(False)
        return panel

    def display(self):
        '''
        Displays window.
        '''
        self.build()
        self.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        self.setResizable(False)
        self.setTitle("Edit settings")
        self.pack()
        self.setLocationRelativeTo(None)
        self.visible = 1
