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

from javax.swing import SpringLayout, JPanel, BoxLayout, ImageIcon, JDialog
from javax.swing import JFrame, JLabel, JComboBox, JTextField, JList, JButton
from java.awt.event import ActionListener
from java.awt import Dimension, Dialog
from ..utils import find_image_resource


class NewAtfView(JDialog):
    '''
    Prompt user to choose some options to create a template for a new ATF
    file.
    '''
    def __init__(self, controller, projects, languages, protocols):
        self.modalityType = Dialog.ModalityType.APPLICATION_MODAL
        self.controller = controller
        self.projects = projects
        self.languages = languages
        self.protocols = protocols
        self.cancelled = False
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
        layout = BoxLayout(self.getContentPane(), BoxLayout.Y_AXIS)
        self.setLayout(layout)

        # Create all necessary panels
        ampersand_panel = self.build_ampersand_row()
        project_panel = self.build_projects_row()
        language_panel = self.build_language_row()
        buttons_panel = self.build_buttons_row()

        # Add panels to main JFrame
        self.add(ampersand_panel)
        self.add(project_panel)
        self.add(language_panel)
        self.add(buttons_panel)

    def build_ampersand_row(self):
        '''
        Builds the &-line row.
        '''
        # Build own panel with SpringLayout.
        panel = JPanel()
        layout = SpringLayout()
        panel.setLayout(layout)
        # Create necessary components and add them to panel.
        ampersand_label = JLabel("CDLI's ID: ")
        self.left_field = JTextField('&')
        equals_label = JLabel('=')
        self.right_field = JTextField()
        tooltip_text = ("<html><body>This is the ID and text's designation "
                        "according to<br/>the CDLI catalog. If your text is "
                        "not yet in the<br/>catalog, please email "
                        "cdli@cdli.ucla.edu to get<br/>an ID and designation."
                        )
        help_label = self.build_help_label(tooltip_text)
        panel.add(ampersand_label)
        panel.add(self.left_field)
        panel.add(equals_label)
        panel.add(self.right_field)
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
                             self.left_field,
                             90,
                             SpringLayout.WEST,
                             panel)
        layout.putConstraint(SpringLayout.NORTH,
                             self.left_field,
                             20,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             equals_label,
                             5,
                             SpringLayout.EAST,
                             self.left_field)
        layout.putConstraint(SpringLayout.NORTH,
                             equals_label,
                             23,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             self.right_field,
                             5,
                             SpringLayout.EAST,
                             equals_label)
        layout.putConstraint(SpringLayout.NORTH,
                             self.right_field,
                             20,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             help_label,
                             5,
                             SpringLayout.EAST,
                             self.right_field)
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
        return panel

    def build_projects_row(self):
        '''
        Builds the projects row.
        '''
        # Build own panel with SpringLayout.
        panel = JPanel()
        layout = SpringLayout()
        panel.setLayout(layout)
        # Create necessary components and add them to panel.
        project_label = JLabel('Project: ')
        self.right_combo = JComboBox()
        self.right_combo.setEditable(True)

        def create_project_list():
            '''
            Prepares list of projects and subprojects ordered with the default
            one first.
            '''
            default_project = self.projects['default'][0].split('/')[0]
            if '/' in self.projects['default']:
                default_subproject = self.projects['default'].split('/')[1]
            else:
                default_subproject = ''
            projects = [default_project]
            subprojects = [default_subproject]
            # User created projects might not be in default dictionary
            for project in self.projects.keys():
                if (project != default_project and project != 'default'):
                    projects.append(project)
                # Default project might not have subproject
            if default_project in self.projects.keys():
                if default_subproject:
                    for subproject in self.projects[default_project]:
                        if (subproject != default_subproject):
                            subprojects.append(subproject)
            return projects, subprojects

        self.left_combo = JComboBox(create_project_list()[0])
        # Make left combo keep size no matter how long project names are
        self.left_combo.setPreferredSize(Dimension(125, 30))
        self.left_combo.setMinimumSize(self.left_combo.getPreferredSize())
        self.left_combo.setMaximumSize(self.left_combo.getPreferredSize())
        self.left_combo.setSize(self.left_combo.getPreferredSize())

        self.right_combo = JComboBox(create_project_list()[1])
        # Prevent right combo to change sizes dynamically
        self.right_combo.setPreferredSize(Dimension(100, 30))
        self.right_combo.setMinimumSize(self.left_combo.getPreferredSize())
        self.right_combo.setMaximumSize(self.left_combo.getPreferredSize())
        self.right_combo.setSize(self.left_combo.getPreferredSize())

        action_listener = ComboActionListener(self.right_combo,
                                              self.projects)
        self.left_combo.addActionListener(action_listener)
        self.left_combo.setEditable(True)
        self.right_combo.setEditable(True)

        slash_label = JLabel('/')

        tooltip_text = ("<html><body>Choose project from list or insert a new "
                        "one.<br/>You can leave the right-hand field blank."
                        "</body><html>")
        help_label = self.build_help_label(tooltip_text)
        panel.add(project_label)
        panel.add(self.left_combo)
        panel.add(slash_label)
        panel.add(self.right_combo)
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
                             self.left_combo,
                             90,
                             SpringLayout.WEST,
                             panel)
        layout.putConstraint(SpringLayout.NORTH,
                             self.left_combo,
                             15,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             slash_label,
                             5,
                             SpringLayout.EAST,
                             self.left_combo)
        layout.putConstraint(SpringLayout.NORTH,
                             slash_label,
                             18,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             self.right_combo,
                             5,
                             SpringLayout.EAST,
                             slash_label)
        layout.putConstraint(SpringLayout.NORTH,
                             self.right_combo,
                             15,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             help_label,
                             5,
                             SpringLayout.EAST,
                             self.right_combo)
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
        return panel

    def build_language_row(self):
        '''
        Builds the language row.
        '''
        # Build own panel with SpringLayout.
        panel = JPanel()
        layout = SpringLayout()
        panel.setLayout(layout)
        # Get language list from settings.yaml, removing the default one from
        # the list
        languages = self.languages.keys()
        languages.remove('default')
        # Create necessary components and add them to panel.
        language_label = JLabel('Language: ')
        self.language_combo = JComboBox(languages)
        # Set selected language to default
        self.language_combo.setSelectedItem(self.languages['default'])
        tooltip_text = "Choose a language from the dropdown menu."
        help_label = self.build_help_label(tooltip_text)
        panel.add(language_label)
        panel.add(self.language_combo)
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
                             self.language_combo,
                             90,
                             SpringLayout.WEST,
                             panel)
        layout.putConstraint(SpringLayout.NORTH,
                             self.language_combo,
                             15,
                             SpringLayout.NORTH,
                             panel)
        layout.putConstraint(SpringLayout.WEST,
                             help_label,
                             5,
                             SpringLayout.EAST,
                             self.language_combo)
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
        return panel

    def build_buttons_row(self):
        '''
        Add OK/Cancel/Blank buttons.
        '''
        # Build own panel with SpringLayout.
        panel = JPanel()
        layout = SpringLayout()
        panel.setLayout(layout)
        # Create necessary components and add them to panel.
        create_button = JButton('Create template',
                                actionPerformed=self.create_template)
        leave_button = JButton('Leave blank', actionPerformed=self.blank)
        cancel_button = JButton('Cancel', actionPerformed=self.cancel)
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
        return panel

    def build_help_label(self, tooltip_text):
        icon = ImageIcon(find_image_resource('smallhelp'))
        label = JLabel()
        label.setIcon(icon)
        label.setToolTipText(tooltip_text)
        return label

    def cancel(self, event):
        self.cancelled = True
        self.dispose()

    def blank(self, event):
        self.controller.show_template()
        self.dispose()

    def create_template(self, event):
        '''
        Put together user selected elements of the template following ATF
        file format.
        '''
        # &-line
        # E.g. &X001001 = JCS 48, 089
        and_line = "{} = {}".format(self.left_field.getText().encode('utf-8'),
                                    self.right_field.getText().encode('utf-8'))

        # Project line
        # E.g. #project: cams/gkab
        # E.g. #project: rimanum
        project_line = "#project: {}".format(
                            self.left_combo.getSelectedItem().encode('utf-8'))
        if self.right_combo.getSelectedItem():
            project_line = "{}/{}".format(
                            project_line,
                            self.right_combo.getSelectedItem().encode('utf-8'))

        # Language line
        # E.g. #atf: lang akk-x-stdbab
        language = self.language_combo.getSelectedItem()
        language_code = self.languages[language]

        # Protocol line/s
        # E.g. #atf: use unicode
        protocols = ''
        for protocol in self.protocols:
            protocols += '#atf: use {}\n'.format(protocol)

        # Put together all lines to create the template and show in ATF area
        self.controller.template = ('{}\n'
                                    '{}\n'
                                    '#atf: lang {}\n'
                                    '{}\n'.format(and_line, project_line,
                                                  language_code, protocols)
                                    )
        self.controller.show_template()
        self.dispose()


class ComboActionListener(ActionListener):
    '''
    Handle dynamically loading right side combo depending on what user chooses
    in left hand combo.
    Note normally can be directly assigned to actionPerformed, but not with
    JComboBox because Jython.
    '''
    def __init__(self, right_combo, projects):
        super(ComboActionListener, self).__init__()
        self.right_combo = right_combo
        self.projects = projects

    def actionPerformed(self, event):
        project = event.getSource().getSelectedItem()
        self.right_combo.removeAllItems()
        # In case they type a new project
        try:
            subprojects = self.projects[project]
        except KeyError:
            return
        # Populate combo box only if project has subprojects
        if subprojects:
            for subproject in subprojects:
                self.right_combo.addItem(subproject)
