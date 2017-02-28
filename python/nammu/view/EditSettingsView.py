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
import re
from java.awt import GridLayout, Component, FlowLayout, Color, BorderLayout
from javax.swing import JDialog, JFrame, JTabbedPane, JComponent, JPanel
from javax.swing import JLabel, BoxLayout, JTextField, JComboBox, JButton


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
        self.setLayout(BorderLayout())
        self.add(self.build_tabbed_panel(), BorderLayout.CENTER)
        self.add(self.build_buttons_panel(), BorderLayout.SOUTH)

    def build_tabbed_panel(self):
        '''
        Build panel with tabs for each of the settings editable sections.
        '''
        tabbed_pane = JTabbedPane()
        tab_titles = ["General", "Keystrokes", "Languages", "Projects"]
        for title in tab_titles:
            panel = self.build_settings_panel(title.lower())
            tabbed_pane.addTab(title, panel)
        return tabbed_pane

    def build_settings_panel(self, text):
        '''
        Call correspondent method to create panel for given tab text.
        '''
        panel = getattr(self, "build_{}_panel".format(text))()
        return panel

    def build_general_panel(self):
        '''
        Create the panel that'll go in the General tab. This should contain
        options for choosing which server to use for validation as well as
        default working dir.
        '''
        panel = JPanel()
        layout = BoxLayout(panel, BoxLayout.Y_AXIS)
        panel.setLayout(layout)
        panel.add(self.build_working_dir_panel())
        panel.add(self.build_servers_panel())
        return panel

    def build_servers_panel(self):
        '''
        Create panel that contains a drop down with the servers to choose from.
        '''
        panel = JPanel(FlowLayout())
        label = JLabel("ORACC server location:")
        panel.add(label)
        self.combo = JComboBox()
        # Go through list of servers and add to combo box.
        for server in self.servers.keys():
            if server != "default":
                self.combo.addItem("{}: {}:{}".format(
                                                server,
                                                self.servers[server]['url'],
                                                self.servers[server]['port']))
        # Make default server the selected item in combo box.
        self.combo.setSelectedItem(self.servers['default'])
        panel.add(self.combo)
        return panel

    def build_working_dir_panel(self):
        '''
        Creates a panel to select preferred working directory.
        '''
        panel = JPanel(FlowLayout())
        label = JLabel("Working directory:")
        panel.add(label)
        self.field = JTextField(40)
        self.field.setText(self.working_dir['default'])
        panel.add(self.field)
        return panel

    def build_buttons_panel(self):
        '''
        Builds the buttons panel to save or cancel changes.
        TODO: Reset button to reset to defaults?
        '''
        panel = JPanel(FlowLayout())
        panel.add(JButton('Cancel', actionPerformed=self.cancel))
        panel.add(JButton('Save', actionPerformed=self.save))
        return panel

    def build_keystrokes_panel(self):
        '''
        Create the panel that'll go in the Keystrokes tab. This should contain
        options for choosing which keystrokes are to be assigned to which
        actions.
        '''
        panel = JPanel()
        return panel

    def build_languages_panel(self):
        '''
        Create the panel that'll go in the Languages tab. This should contain
        options for choosing which is the list of languages that can be
        included from the new ATF window and their abbrv.
        '''
        panel = JPanel()
        return panel

    def build_projects_panel(self):
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

    def cancel(self, event=None):
        '''
        Close window and don't save changes.
        '''
        self.dispose()

    def save(self, event=None):
        '''
        Save changes made by user on local settings file.
        '''
        # Update only the working_dir and the server for now
        # TODO: update keystrokes, projects list, etc.
        working_dir = self.field.getText()
        # The server format is "name: url:port". We only need "name"
        server = re.split(self.combo.getSelectedItem(), ':')[0]
        self.controller.update_config(working_dir, server)
        # Close window
        self.dispose()
