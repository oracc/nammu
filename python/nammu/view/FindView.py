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
from javax.swing import SpringLayout, JPanel, BoxLayout, ImageIcon, JDialog
from javax.swing import JFrame, JLabel, JComboBox, JTextField, JList, JButton
from java.awt import Dimension, Dialog, BorderLayout, FlowLayout
from ..utils import find_image_resource

class FindView(JDialog):
    '''
    Prompt user to choose some options to find and replace text in ATF area.
    '''
    def __init__(self, controller):
        self.logger = logging.getLogger("NammuController")
        self.modalityType = Dialog.ModalityType.APPLICATION_MODAL
        self.controller = controller
        self.pane = self.getContentPane()

    def display(self):
        '''
        Displays window.
        '''
        self.build()
        self.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        self.setResizable(False)
        self.setTitle("Find/Replace")
        self.pack()
        self.setLocationRelativeTo(None)
        self.visible = 1

    def build(self):
        layout = BoxLayout(self.getContentPane(), BoxLayout.Y_AXIS)
        self.setLayout(layout)

        # Create all necessary panels
        find_panel = self.build_find_row()
        replace_panel = self.build_replace_row()
        # replace_panel = self.build_find_panel()

        # Add panels to main JFrame
        # self.add(find_panel)
        # self.add(replace_panel)
        self.add(self.build_find_replace_rows())

    def build_find_replace_rows(self):
        labels = ("Find: ", "Replace: ")

        # Create and populate the panel.
        panel = JPanel()
        for label in labels:
            row_panel = JPanel(BorderLayout())
            label = JLabel(label, JLabel.TRAILING)
            row_panel.add(label, BorderLayout.WEST)
            textfield = JTextField(20)
            label.setLabelFor(textfield)
            row_panel.add(textfield, BorderLayout.CENTER)
            panel.add(row_panel)

        return panel

    def build_find_row(self):
        '''
        Builds the find row.
        '''
        # Build own panel with SpringLayout.
        panel = JPanel()
        layout = SpringLayout()
        panel.setLayout(layout)
        # Create necessary components and add them to panel.
        label = JLabel("Find: ")
        self.field = JTextField(20)
        panel.add(label)
        panel.add(self.field)
        # Set up constraints to tell panel how to position components.
        layout.putConstraint(SpringLayout.WEST,
                             label,
                             10,
                             SpringLayout.WEST,
                             panel)
        layout.putConstraint(SpringLayout.NORTH,
                             label,
                             10,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.EAST,
                             self.field,
                             10,
                             SpringLayout.EAST,
                             panel)
        layout.putConstraint(SpringLayout.NORTH,
                             self.field,
                             8,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.EAST,
                             panel,
                             400,
                             SpringLayout.WEST,
                             label)
        layout.putConstraint(SpringLayout.SOUTH,
                             panel,
                             5,
                             SpringLayout.SOUTH,
                             self.field)
        # Add this to NewAtf JFrame
        return panel

    def build_replace_row(self):
        '''
        Builds the replace row.
        '''
        # Build own panel with SpringLayout.
        panel = JPanel()
        layout = SpringLayout()
        panel.setLayout(layout)
        # Create necessary components and add them to panel.
        label = JLabel("Replace: ")
        self.field = JTextField(20)
        panel.add(label)
        panel.add(self.field)
        # Set up constraints to tell panel how to position components.
        layout.putConstraint(SpringLayout.WEST,
                             label,
                             10,
                             SpringLayout.WEST,
                             panel)
        layout.putConstraint(SpringLayout.NORTH,
                             label,
                             10,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.EAST,
                             self.field,
                             10,
                             SpringLayout.EAST,
                             panel)
        layout.putConstraint(SpringLayout.NORTH,
                             self.field,
                             8,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.EAST,
                             panel,
                             400,
                             SpringLayout.WEST,
                             label)
        layout.putConstraint(SpringLayout.SOUTH,
                             panel,
                             5,
                             SpringLayout.SOUTH,
                             self.field)

        # Add this to NewAtf JFrame
        return panel
