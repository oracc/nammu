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
from java.awt import GridLayout, Component, FlowLayout, Color
from javax.swing import JDialog, JFrame, JTabbedPane, JComponent, JPanel
from javax.swing import JLabel, BoxLayout, JTextField, JComboBox


class EditSettingsView(JDialog):
    def __init__(self, controller, working_dir, servers, keystrokes,
                 languages, projects):
        self.logger = logging.getLogger("NammuController")
        self.setAlwaysOnTop(True)
        self.controller = controller
        self.working_dir = working_dir
        self.servers = servers
        self.keystrokes = keystrokes
        self.languages = languages
        self.projects = projects
        self.pane = self.getContentPane()

    def build(self):
        '''
        Create all tab panels and put together to form the settings window.
        '''
        self.setLayout(GridLayout(1, 1))
        tabbedPane = JTabbedPane()
        tab_titles = ["General", "Keystrokes", "Languages", "Projects"]
        for title in tab_titles:
            panel = self.build_settings_pane(title.lower())
            tabbedPane.addTab(title, panel)
        self.add(tabbedPane)

    def build_settings_pane(self, text):
        '''
        Call correspondent method to create panel for given tab text.
        '''
        panel = getattr(self, "build_{}_pane".format(text))()
        return panel

    def build_general_pane(self):
        '''
        Create the panel that'll go in the General tab. This should contain
        options for choosing which server to use for validation as well as
        default working dir.
        '''
        panel = JPanel()
        layout = BoxLayout(panel, BoxLayout.Y_AXIS)
        panel.setLayout(layout)
        dir_panel = JPanel(FlowLayout())
        dir_label = JLabel("Working directory:")
        dir_panel.add(dir_label)
        dir_field = JTextField(20)
        dir_panel.add(dir_field)
        server_panel = JPanel(FlowLayout())
        server_label = JLabel("Server:")
        server_panel.add(server_label)
        server_combo = JComboBox()
        for server in self.servers.keys():
            if server != "default":
                server_combo.addItem("{}: {}:{}".format(
                                                server,
                                                self.servers[server]['url'],
                                                self.servers[server]['port']))
        server_panel.add(server_combo)
        panel.add(dir_panel)
        panel.add(server_panel)
        return panel

    def build_keystrokes_pane(self):
        '''
        Create the panel that'll go in the Keystrokes tab. This should contain
        options for choosing which keystrokes are to be assigned to which
        actions.
        '''
        panel = JPanel()
        return panel

    def build_languages_pane(self):
        '''
        Create the panel that'll go in the Languages tab. This should contain
        options for choosing which is the list of languages that can be
        included from the new ATF window and their abbrv.
        '''
        panel = JPanel()
        return panel

    def build_projects_pane(self):
        '''
        Create the panel that'll go in the Projects tab. This should contain
        the list of preferred projects and a means to select which is the
        preferred default.
        '''
        panel = JPanel()

        return panel

    def display(self):
        '''
        Displays window.
        '''
        self.build()
        self.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        self.setResizable(True)
        self.setTitle("Edit settings")
        self.pack()
        self.setLocationRelativeTo(None)
        self.visible = 1

    def display_error(self, keyword):
        '''
        Display error message when keyword is not in settings file.
        '''
        pass
