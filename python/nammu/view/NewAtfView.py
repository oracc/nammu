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

from java.awt import GridLayout
from javax.swing import SpringLayout, JPanel
from javax.swing import JFrame, JLabel, JComboBox, JTextField, JList, JButton


class NewAtfView(JFrame):
    '''
    Prompt user to choose some options to create a template for a new ATF
    file.
    '''
    def __init__(self, controller, projects, languages, protocols):
        self.controller = controller
        self.projects = projects
        self.languages = languages
        self.protocols = protocols
        self.springLayout = SpringLayout()
        self.pane = self.getContentPane()

    def display(self):
        '''
        Displays window.
        '''
        self.build()
        self.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        self.setResizable(False)
        self.setTitle("New ATF template")
        self.pack()
        self.setLocationRelativeTo(None)
        self.visible = 1

    def build(self):
        '''
        Puts all the window components together in the JFrame
        '''
        self.setLayout(GridLayout(4, 1))
        self.add_ampersand_row()
        self.add_projects_row()
        self.add_language_row()
#         self.add_protocols_row()
        self.add_buttons_row()

    def add_ampersand_row(self):
        '''
        Builds the &-line row.
        '''
        # Build own panel with SpringLayout.
        panel = JPanel()
        layout = SpringLayout()
        panel.setLayout(layout)
        # Create necessary components and add them to panel.
        ampersand_label = JLabel("CDLI's ID: ")
        left_field = JTextField('&...')
        equals_label = JLabel('=')
        right_field = JTextField()
        help_label = JLabel('?')
        panel.add(ampersand_label)
        panel.add(left_field)
        panel.add(equals_label)
        panel.add(right_field)
        panel.add(help_label)
        # Set up constraints to tell panel how to position components.
        layout.putConstraint(SpringLayout.WEST,
                             ampersand_label,
                             20,
                             SpringLayout.WEST,
                             panel)
        layout.putConstraint(SpringLayout.NORTH,
                             ampersand_label,
                             23,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             left_field,
                             90,
                             SpringLayout.WEST,
                             panel)
        layout.putConstraint(SpringLayout.NORTH,
                             left_field,
                             20,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             equals_label,
                             5,
                             SpringLayout.EAST,
                             left_field)
        layout.putConstraint(SpringLayout.NORTH,
                             equals_label,
                             23,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             right_field,
                             5,
                             SpringLayout.EAST,
                             equals_label)
        layout.putConstraint(SpringLayout.NORTH,
                             right_field,
                             20,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             help_label,
                             5,
                             SpringLayout.EAST,
                             right_field)
        layout.putConstraint(SpringLayout.NORTH,
                             help_label,
                             23,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.EAST,
                             panel,
                             15,
                             SpringLayout.EAST,
                             help_label)
        layout.putConstraint(SpringLayout.SOUTH,
                             panel,
                             10,
                             SpringLayout.SOUTH,
                             help_label)
        # Add this to NewAtf JFrame
        self.add(panel)

    def add_projects_row(self):
        '''
        Builds the projects row.
        '''
        # Build own panel with SpringLayout.
        panel = JPanel()
        layout = SpringLayout()
        panel.setLayout(layout)
        # Create necessary components and add them to panel.
        project_label = JLabel('Project: ')
        left_combo = JComboBox(self.projects.keys())
        slash_label = JLabel('/')
        right_combo = JComboBox()
        help_label = JLabel('?')
        panel.add(project_label)
        panel.add(left_combo)
        panel.add(slash_label)
        panel.add(right_combo)
        panel.add(help_label)
        # Set up constraints to tell panel how to position components.
        layout.putConstraint(SpringLayout.WEST,
                             project_label,
                             15,
                             SpringLayout.WEST,
                             panel)
        layout.putConstraint(SpringLayout.NORTH,
                             project_label,
                             18,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             left_combo,
                             90,
                             SpringLayout.WEST,
                             panel)
        layout.putConstraint(SpringLayout.NORTH,
                             left_combo,
                             15,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             slash_label,
                             5,
                             SpringLayout.EAST,
                             left_combo)
        layout.putConstraint(SpringLayout.NORTH,
                             slash_label,
                             18,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             right_combo,
                             5,
                             SpringLayout.EAST,
                             slash_label)
        layout.putConstraint(SpringLayout.NORTH,
                             right_combo,
                             15,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             help_label,
                             5,
                             SpringLayout.EAST,
                             right_combo)
        layout.putConstraint(SpringLayout.NORTH,
                             help_label,
                             18,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.EAST,
                             panel,
                             15,
                             SpringLayout.EAST,
                             help_label)
        layout.putConstraint(SpringLayout.SOUTH,
                             panel,
                             10,
                             SpringLayout.SOUTH,
                             help_label)
        # Add this to NewAtf JFrame
        self.add(panel)

    def add_language_row(self):
        '''
        Builds the language row.
        '''
        # Build own panel with SpringLayout.
        panel = JPanel()
        layout = SpringLayout()
        panel.setLayout(layout)
        # Create necessary components and add them to panel.
        language_label = JLabel('Language: ')
        language_combo = JComboBox(self.languages.keys())
        help_label = JLabel('?')
        panel.add(language_label)
        panel.add(language_combo)
        panel.add(help_label)
        # Set up constraints to tell panel how to position components.
        layout.putConstraint(SpringLayout.WEST,
                             language_label,
                             15,
                             SpringLayout.WEST,
                             panel)
        layout.putConstraint(SpringLayout.NORTH,
                             language_label,
                             18,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             language_combo,
                             90,
                             SpringLayout.WEST,
                             panel)
        layout.putConstraint(SpringLayout.NORTH,
                             language_combo,
                             15,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             help_label,
                             5,
                             SpringLayout.EAST,
                             language_combo)
        layout.putConstraint(SpringLayout.NORTH,
                             help_label,
                             18,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.EAST,
                             panel,
                             15,
                             SpringLayout.EAST,
                             help_label)
        layout.putConstraint(SpringLayout.SOUTH,
                             panel,
                             10,
                             SpringLayout.SOUTH,
                             help_label)
        # Add this to NewAtf JFrame
        self.add(panel)

    def add_protocols_row(self):
        '''
        Builds the protocols row.
        '''
        # Build own panel with SpringLayout.
        panel = JPanel()
        layout = SpringLayout()
        panel.setLayout(layout)
        # Create necessary components and add them to panel.
        protocols_label = JLabel('Protocols: ')
        protocols_list = JList(self.protocols)
        help_label = JLabel('?')
        panel.add(protocols_label)
        panel.add(protocols_list)
        panel.add(help_label)
        # Set up constraints to tell panel how to position components.
        layout.putConstraint(SpringLayout.WEST,
                             protocols_label,
                             15,
                             SpringLayout.WEST,
                             panel)
        layout.putConstraint(SpringLayout.NORTH,
                             protocols_label,
                             18,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             protocols_list,
                             90,
                             SpringLayout.WEST,
                             panel)
        layout.putConstraint(SpringLayout.NORTH,
                             protocols_list,
                             15,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             help_label,
                             5,
                             SpringLayout.EAST,
                             protocols_list)
        layout.putConstraint(SpringLayout.NORTH,
                             help_label,
                             18,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.EAST,
                             panel,
                             15,
                             SpringLayout.EAST,
                             help_label)
        layout.putConstraint(SpringLayout.SOUTH,
                             panel,
                             10,
                             SpringLayout.SOUTH,
                             protocols_label)
        # Add this to NewAtf JFrame
        self.add(panel)

    def add_buttons_row(self):
        '''
        Add OK/Cancel/Blank buttons.
        '''
        # Build own panel with SpringLayout.
        panel = JPanel()
        layout = SpringLayout()
        panel.setLayout(layout)
        # Create necessary components and add them to panel.
        create_button = JButton('Create template')
        leave_button = JButton('Leave blank')
        cancel_button = JButton('Cancel')
        panel.add(create_button)
        panel.add(leave_button)
        panel.add(cancel_button)

        # Set up constraints to tell panel how to position components.
        layout.putConstraint(SpringLayout.WEST,
                             create_button,
                             15,
                             SpringLayout.WEST,
                             panel)
        layout.putConstraint(SpringLayout.NORTH,
                             create_button,
                             15,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             leave_button,
                             5,
                             SpringLayout.EAST,
                             create_button)
        layout.putConstraint(SpringLayout.NORTH,
                             leave_button,
                             15,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             cancel_button,
                             5,
                             SpringLayout.EAST,
                             leave_button)
        layout.putConstraint(SpringLayout.NORTH,
                             cancel_button,
                             15,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.EAST,
                             panel,
                             15,
                             SpringLayout.EAST,
                             cancel_button)
        layout.putConstraint(SpringLayout.SOUTH,
                             panel,
                             10,
                             SpringLayout.SOUTH,
                             cancel_button)
        # Add this to NewAtf JFrame
        self.add(panel)
