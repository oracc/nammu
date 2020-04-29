# -*- coding: utf-8 -*-
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

import logging
from javax.swing import SpringLayout, JPanel, BoxLayout, JDialog
from javax.swing import JFrame, JLabel, JTextField, JButton
from javax.swing import JCheckBox, KeyStroke, AbstractAction, JComponent
from java.awt import FlowLayout, Toolkit
from java.awt.event import KeyEvent


class FindView(JDialog):
    '''
    Prompt user to choose some options to find and replace text in ATF area.
    '''
    def __init__(self, controller):
        self.logger = logging.getLogger("NammuController")
        self.setAlwaysOnTop(True)
        self.controller = controller
        self.pane = self.getContentPane()

        # Get key bindings configuration from settings
        key_strokes = self.controller.config['find_keystrokes']

        # Configure key bindings for undo/redo
        # First decide when key bindings can be triggered:
        condition = JComponent.WHEN_IN_FOCUSED_WINDOW

        # InputMap maps key strokes to actions in string format (e.g. 'undo')
        # ActionMap maps string actions (e.g. 'undo') with a custom
        # AbstractAction subclass.
        pane = self.getContentPane()
        for action, key in key_strokes.iteritems():
            key_stroke = KeyStroke.getKeyStroke(
                        getattr(KeyEvent, key),
                        Toolkit.getDefaultToolkit().getMenuShortcutKeyMask())
            pane.getInputMap(condition).put(key_stroke, action)
            pane.getActionMap().put(action, KeyStrokeAction(self, action))

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
        options_panel = self.build_options_row()
        buttons_panel = self.build_buttons_row()
        # replace_panel = self.build_find_panel()

        # Add panels to main JFrame
        self.add(find_panel)
        self.add(replace_panel)
        self.add(options_panel)
        self.add(buttons_panel)
        # self.add(self.build_find_replace_rows())

    def build_find_replace_rows(self):
        labels = ("Find: ", "Replace: ")

        # Create and populate the panel.
        panel = JPanel()
        for label in labels:
            row_panel = JPanel(FlowLayout())
            label = JLabel(label, JLabel.TRAILING)
            row_panel.add(label, FlowLayout.LEFT)
            textfield = JTextField(20)
            label.setLabelFor(textfield)
            row_panel.add(textfield, FlowLayout.RIGHT)
            panel.add(row_panel)

        return panel

    def build_find_row(self):
        '''
        Builds the find row.
        '''
        panel = JPanel(FlowLayout())
        label = JLabel("Find:     ")
        panel.add(label)
        self.find_field = JTextField(20, actionPerformed=self.find_next)
        label.setLabelFor(self.find_field)
        panel.add(self.find_field)
        return panel

    def build_replace_row(self):
        '''
        Builds the replace row.
        '''
        panel = JPanel(FlowLayout())
        label = JLabel("Replace: ")
        panel.add(label)
        self.replace_field = JTextField(20, actionPerformed=self.find_next)
        label.setLabelFor(self.replace_field)
        panel.add(self.replace_field)
        return panel

    def build_options_row(self):
        '''
        Builds the panel with ignore case, regex, etc. options.
        '''
        panel = JPanel(FlowLayout())
        self.ignore_case_box = JCheckBox('Ignore Case')
        self.regex_box = JCheckBox('Regular Expression')
        self.selection_box = JCheckBox('Selection only')
        panel.add(self.ignore_case_box)
        panel.add(self.regex_box)
        panel.add(self.selection_box)
        return panel

    def build_buttons_row(self):
        '''
        Builds the buttons row.
        '''
        panel = JPanel()
        layout = SpringLayout()
        panel.setLayout(layout)
        # Create necessary components and add them to panel.
        find_next_button = JButton('Find Next',
                                   actionPerformed=self.find_next)
        replace_one_button = JButton('Replace',
                                     actionPerformed=self.replace_one)
        replace_all_button = JButton('Replace All',
                                     actionPerformed=self.replace_all)
        done_button = JButton('Done', actionPerformed=self.done)
        panel.add(find_next_button)
        panel.add(replace_one_button)
        panel.add(replace_all_button)
        panel.add(done_button)

        # Set up constraints to tell panel how to position components.
        layout.putConstraint(SpringLayout.WEST,
                             find_next_button,
                             15,
                             SpringLayout.WEST,
                             panel)
        layout.putConstraint(SpringLayout.NORTH,
                             find_next_button,
                             15,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             replace_one_button,
                             5,
                             SpringLayout.EAST,
                             find_next_button)
        layout.putConstraint(SpringLayout.NORTH,
                             replace_one_button,
                             15,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             replace_all_button,
                             5,
                             SpringLayout.EAST,
                             replace_one_button)
        layout.putConstraint(SpringLayout.NORTH,
                             replace_all_button,
                             15,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             done_button,
                             5,
                             SpringLayout.EAST,
                             replace_all_button)
        layout.putConstraint(SpringLayout.NORTH,
                             done_button,
                             15,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.EAST,
                             panel,
                             15,
                             SpringLayout.EAST,
                             done_button)
        layout.putConstraint(SpringLayout.SOUTH,
                             panel,
                             10,
                             SpringLayout.SOUTH,
                             done_button)
        # Add this to NewAtf JFrame
        return panel

    def find_next(self, event=None):
        self.controller.find_next(self.find_field.getText(),
                                  self.ignore_case_box.isSelected(),
                                  self.regex_box.isSelected(),
                                  self.selection_box.isSelected())

    def replace_one(self, event=None):
        self.controller.replace_one(self.find_field.getText(),
                                    self.replace_field.getText(),
                                    self.ignore_case_box.isSelected(),
                                    self.regex_box.isSelected(),
                                    self.selection_box.isSelected())

    def replace_all(self, event=None):
        self.controller.replace_all(self.find_field.getText(),
                                    self.replace_field.getText(),
                                    self.ignore_case_box.isSelected(),
                                    self.regex_box.isSelected(),
                                    self.selection_box.isSelected())

    def done(self, event):
        '''
        Reset list of matches and close window.
        '''
        self.controller.matches = None
        self.controller.text = None
        self.controller.controller.find_controller = None
        self.controller.atfAreaController.restore_highlight()
        self.dispose()


class KeyStrokeAction(AbstractAction):
    '''
    Needed to be assigned to key strokes via JComponent's ActionMap.
    '''
    def __init__(self, component, action):
        self.component = component
        self.action = action

    def actionPerformed(self, event):
        '''
        Overrides AbstractAction's actionPerform to executed the given action
        in the component's controller.
        '''
        getattr(self.component, self.action)()
