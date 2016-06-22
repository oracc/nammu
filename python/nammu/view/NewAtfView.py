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
        self.setTitle("New ATF template")
        self.pack()
        self.setLocationRelativeTo(None)
        self.visible = 1

    def build(self):
        '''
        Puts all the window components together in the JFrame
        '''
        self.setLayout(GridLayout(1, 4))
#         self.add_and_row()
#         self.add_projects_row()
        self.add_language_row()
#         self.add_protocols_row()
#         self.add_buttons_row()
#         self.setLayout(self.layout)

    def add_and_row(self):
        '''
        Builds the &-line row.
        '''
        self.add(JLabel('&'))
        self.add(JTextField())
        self.add(JLabel('='))
        self.add(JTextField())
        self.add(JLabel('?'))

    def add_projects_row(self):
        '''
        Builds the projects row.
        '''
        self.add(JLabel('project: '))
        self.add(JComboBox(self.projects.keys()))
        self.add(JLabel('/'))
        self.add(JComboBox())
        self.add(JLabel('?'))

    def add_language_row(self):
        '''
        Builds the language row.
        '''
        panel = JPanel()
        layout = SpringLayout()
        panel.setLayout(layout)
        
        language_label = JLabel('language: ')
        language_combo = JComboBox(self.languages.keys())
        help_label = JLabel('?')
        
        panel.add(language_label)
        panel.add(language_combo)
        panel.add(help_label)
        
        layout.putConstraint(SpringLayout.WEST,
                             language_label,
                             15,
                             SpringLayout.WEST,
                             panel)
        layout.putConstraint(SpringLayout.NORTH,
                             language_label,
                             9,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             language_combo,
                             5,
                             SpringLayout.EAST,
                             language_label)
        layout.putConstraint(SpringLayout.NORTH,
                             language_combo,
                             5,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             help_label,
                             5,
                             SpringLayout.EAST,
                             language_combo)
        layout.putConstraint(SpringLayout.NORTH,
                             help_label,
                             9,
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
        
        self.add(panel)

    def add_protocols_row(self):
        '''
        Builds the protocols row.
        '''
        self.add(JLabel('protocols: '))
        self.add(JList(self.protocols))
        self.add(JLabel('?'))

    def add_buttons_row(self):
        '''
        Add OK/Cancel/Blank buttons.
        '''
        self.add(JButton('Create template'))
        self.add(JButton('Leave blank'))
        self.add(JButton('Cancel'))
