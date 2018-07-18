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
from swingutils.threads.swing import runSwingLater

from java.awt import FlowLayout, BorderLayout, Insets
from java.awt import GridBagLayout, GridBagConstraints
from javax.swing import JDialog, JFrame, JTabbedPane, JPanel
from javax.swing import JLabel, JTextField, JComboBox, JButton
from javax.swing import JFileChooser


class EditSettingsView(JDialog):
    def __init__(self, controller, working_dir, servers, console_style,
                 edit_area_style, keystrokes, languages, projects):
        self.logger = logging.getLogger("NammuController")
        self.setAlwaysOnTop(True)
        self.controller = controller
        self.working_dir = working_dir
        self.servers = servers
        self.keystrokes = keystrokes
        self.languages = languages
        self.projects = projects
        self.console_fontsize = console_style['fontsize']['user']
        self.console_font_color = console_style['font_color']['user']
        self.console_bg_color = console_style['background_color']['user']
        self.edit_area_fontsize = edit_area_style['fontsize']['user']
        self.pane = self.getContentPane()

        # Grab the console color options from the console view
        self.consoleView = self.controller.controller.consoleController.view
        self.color_options = self.consoleView.colors.keys()

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
        tab_titles = ["General", "Appearance", "Keystrokes", "Languages",
                      "Projects"]
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
        panel = JPanel(GridBagLayout())
        constraints = self.add_constraints(GridBagConstraints(),
                                           insets=Insets(10, 10, 10, 10))
        self.build_working_dir_panel(constraints, panel)
        self.build_servers_panel(constraints, panel)
        return panel

    def add_constraints(self, constraints, weightx=None, gridx=None,
                        gridy=None, fill=None, insets=None, gridwidth=None,
                        anchor=None):
        '''
        Wrapper around the various constraints we need to set.
        '''
        # Cant use pythonic truth value test as we need 0 to evaluate as true
        if weightx is not None:
            constraints.weightx = weightx
        if gridx is not None:
            constraints.gridx = gridx
        if gridy is not None:
            constraints.gridy = gridy
        if fill is not None:
            constraints.fill = fill
        if insets is not None:
            constraints.insets = insets
        if gridwidth is not None:
            constraints.gridwidth = gridwidth
        if anchor is not None:
            constraints.anchor = anchor

        return constraints

    def build_working_dir_panel(self, constraints, panel):
        '''
        Working directory row: label + field + button
        This is for users to browse for their preferred default directory
        when opening/creating a new file.
        '''
        working_dir_label = JLabel("Working directory:")
        constraints = self.add_constraints(constraints, weightx=0.30,
                                           gridx=0, gridy=0,
                                           anchor=GridBagConstraints.EAST)

        panel.add(working_dir_label, constraints)

        self.wd_field = JTextField()
        self.wd_field.setEditable(False)
        # Can't find an elegant way to default to something that would be
        # crossplatform, and I can't leave the default field empty.
        if self.working_dir['default'] != "None":
            self.wd_field.setText(self.working_dir['default'])
        else:
            self.wd_field.setText(os.getcwd())

        constraints = self.add_constraints(constraints, weightx=0.60,
                                           gridx=1, gridy=0,
                                           fill=GridBagConstraints.HORIZONTAL,
                                           insets=Insets(10, 10, 10, 5))
        panel.add(self.wd_field, constraints)

        constraints.fill = 0
        button = JButton("Browse", actionPerformed=self.browse)
        constraints = self.add_constraints(constraints, weightx=0.10,
                                           gridx=2, gridy=0,
                                           insets=Insets(10, 0, 10, 10))
        panel.add(button, constraints)

    def build_console_background_color_panel(self, constraints, panel):
        '''
        Server location row: label + dropdown
        Contains a drop down with the servers to choose from.
        '''
        console_bg_label = JLabel("Console background color:")
        constraints = self.add_constraints(constraints, weightx=0.30,
                                           gridx=0, gridy=2)
        panel.add(console_bg_label, constraints)

        self.bg_color_combo = self.build_combobox(self.color_options,
                                                  self.console_bg_color)
        constraints = self.add_constraints(constraints, weightx=0.70,
                                           gridx=1, gridy=2, gridwidth=2,
                                           fill=GridBagConstraints.HORIZONTAL)
        panel.add(self.bg_color_combo, constraints)

    def build_console_font_color_panel(self, constraints, panel):
        '''
        Server location row: label + dropdown
        Contains a drop down with the servers to choose from.
        '''
        console_font_label = JLabel("Console font color:")
        constraints = self.add_constraints(constraints, weightx=0.30,
                                           gridx=0, gridy=3)
        panel.add(console_font_label, constraints)

        self.font_color_combo = self.build_combobox(self.color_options,
                                                    self.console_font_color)
        constraints = self.add_constraints(constraints, weightx=0.70,
                                           gridx=1, gridy=3, gridwidth=2,
                                           fill=GridBagConstraints.HORIZONTAL)
        panel.add(self.font_color_combo, constraints)

    def build_servers_panel(self, constraints, panel):
        '''
        Server location row: label + dropdown
        Contains a drop down with the servers to choose from.
        '''
        server_label = JLabel("ORACC server location:")
        constraints = self.add_constraints(constraints, weightx=0.30,
                                           gridx=0, gridy=1,
                                           insets=Insets(10, 10, 80, 10))
        panel.add(server_label, constraints)

        self.combo = self.build_servers_combobox()
        constraints = self.add_constraints(constraints, weightx=0.70,
                                           gridx=1, gridy=1, gridwidth=2,
                                           fill=GridBagConstraints.HORIZONTAL)
        panel.add(self.combo, constraints)

    def build_console_font_panel(self, constraints, panel):
        '''
        Font size on a textfield.
        '''
        fontzise_label = JLabel("Console font size:")
        constraints = self.add_constraints(constraints, weightx=0.20,
                                           gridx=0, gridy=0,
                                           fill=GridBagConstraints.HORIZONTAL)
        panel.add(fontzise_label, constraints)

        self.fs_field = JTextField()
        self.fs_field.setEditable(True)
        if self.console_fontsize:
            self.fs_field.setText("{}".format(self.console_fontsize))
        else:
            self.fs_field.setText(self.controller.config[
                                    'console_style']['fontsize']['default'])

        constraints = self.add_constraints(constraints, weightx=0.80,
                                           gridx=1, gridy=0,
                                           fill=GridBagConstraints.HORIZONTAL)
        panel.add(self.fs_field, constraints)

    def build_edit_area_font_panel(self, constraints, panel):
        '''
        Font size on a textfield.
        '''
        fontzise_label = JLabel("Edit area font size:")
        constraints = self.add_constraints(constraints, weightx=0.20,
                                           gridx=0, gridy=4)
        panel.add(fontzise_label, constraints)

        self.edit_area_fs_field = JTextField()
        self.edit_area_fs_field.setEditable(True)
        if self.edit_area_fontsize:
            self.edit_area_fs_field.setText(
                                    "{}".format(self.edit_area_fontsize))
        else:
            self.edit_area_fs_field.setText(self.controller.config[
                                    'edit_area_style']['fontsize']['default'])

        constraints = self.add_constraints(constraints, weightx=0.80,
                                           gridx=1, gridy=4,
                                           fill=GridBagConstraints.HORIZONTAL)
        panel.add(self.edit_area_fs_field, constraints)

    def build_combobox(self, choices, default):
        '''
        Generic method to construct a combobox. choices should be an iterable
        of strings of the choices to be made and default should be a string
        which is equal to one of the values within the iterable.
        '''
        combo = JComboBox()
        for choice in choices:
            combo.addItem(choice)
        combo.setSelectedItem(default)
        return combo

    def build_servers_combobox(self):
        combo = JComboBox()
        # Go through list of servers and add to combo box.
        for server in self.servers.keys():
            if server != "default":
                combo_item = "{}: {}:{}".format(server,
                                                self.servers[server]['url'],
                                                self.servers[server]['port'])
                combo.addItem(combo_item)
                # If this item is the default one, set it as selected
                if server == self.servers['default']:
                    combo.setSelectedItem(combo_item)
        return combo

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
        label = JLabel("Coming soon...")
        panel.add(label, BorderLayout.CENTER)
        return panel

    def build_languages_panel(self):
        '''
        Create the panel that'll go in the Languages tab. This should contain
        options for choosing which is the list of languages that can be
        included from the new ATF window and their abbrv.
        '''
        panel = JPanel()
        label = JLabel("Coming soon...")
        panel.add(label, BorderLayout.CENTER)
        return panel

    def build_projects_panel(self):
        '''
        Create the panel that'll go in the Projects tab. This should contain
        the list of preferred projects and a means to select which is the
        preferred default.
        '''
        panel = JPanel()
        label = JLabel("Coming soon...")
        panel.add(label, BorderLayout.CENTER)
        return panel

    def build_appearance_panel(self):
        '''
        Create the panel that'll go in the General tab. This should contain
        options for choosing which server to use for validation as well as
        default working dir.
        '''
        panel = JPanel(GridBagLayout())
        constraints = self.add_constraints(GridBagConstraints(),
                                           insets=Insets(10, 10, 10, 10))
        self.build_console_font_panel(constraints, panel)
        self.build_console_font_color_panel(constraints, panel)
        self.build_console_background_color_panel(constraints, panel)
        self.build_edit_area_font_panel(constraints, panel)
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

    def validate_fontsize(self, input_size, target_key):
        '''
        Method to validate an input fontsize. The target key points to either
        the console font sizes 'console_style' or the edit area font sizes
        'edit_area_style'. If the value is invalid, return the previous user
        fontsize that was stored.
        The second return value is a bool indicating if the value has changed.
        '''
        # Extract plain english from key name for use in error message
        target = target_key[:-6].replace('_', ' ')

        # Use isnumeric() to test if a unicode string only has digits
        if (input_size.isnumeric() and (8 <= int(input_size) <= 30)):
            return input_size, True
        else:
            input_size = self.controller.config[target_key]['fontsize']['user']
            self.logger.error("Invalid {} font size. Please enter a "
                              "number between 8 and 36.\n\n"
                              "Font size left at "
                              "previous value: {}".format(target, input_size))

            return input_size, False

    def validate_colors(self, bg_color, font_color):
        '''
        Validate console colors to ensure they do not match.
        The second return value is a bool indicating if the value has changed.
        '''
        valid = True
        if bg_color == font_color:
            config = self.controller.config
            self.logger.error("Console font colour cannot match background"
                              " colour. Resetting to default values.")
            bg_color = config['console_style']['background_color']['default']
            font_color = config['console_style']['font_color']['default']
            valid = False

        return bg_color, font_color, valid

    def validate_working_dir(self, working_dir):
        '''
        Method to validate input working directories. If directory does not
        exist or if a path to a file is provided instead of a path to a
        directory the method returns None.
        The second return value is a bool indicating if the value has changed.
        '''
        if os.path.isdir(working_dir):
            return working_dir, True
        else:
            self.logger.error("{} is not a valid working directory."
                              " No working directory has been "
                              "saved".format(working_dir))
            return None, False

    def validate_all_inputs(self, working_dir, console_fontsize,
                            edit_area_fontsize, bg_color, font_color):
        '''
        Wrapper around the input validation methods. Returns a tuple containing
        the validated inputs with the last value in the tuple a boolean set to
        False if any of the values have been altered during the validation
        and True if there have been no changes.
        '''
        # Collect the results of each validation. In future we might use this
        # to provide more detailed error logging on bad user input
        validation_results = []

        # Validate the working directory input string
        working_dir, v = self.validate_working_dir(working_dir)
        validation_results.append(v)

        # Validate the input fontsizes
        con_size, v = self.validate_fontsize(console_fontsize, 'console_style')
        validation_results.append(v)

        edit_size, v = self.validate_fontsize(edit_area_fontsize,
                                              'edit_area_style')
        validation_results.append(v)

        # Validate input console colors
        bg_color, font_color, v = self.validate_colors(bg_color, font_color)
        validation_results.append(v)

        return (working_dir, int(con_size), font_color, bg_color,
                int(edit_size), all(validation_results))

    def save(self, event=None):
        '''
        Save changes made by user on local settings file.
        '''
        # Update only the working_dir and the server for now
        # TODO: update keystrokes, projects list, etc.
        working_dir = self.wd_field.getText()

        # Read the fontsize from the textfield
        console_fontsize = self.fs_field.getText()
        edit_area_fontsize = self.edit_area_fs_field.getText()

        # Get the user selected font and background colours
        bg_color = self.bg_color_combo.getSelectedItem()
        font_color = self.font_color_combo.getSelectedItem()

        validated = self.validate_all_inputs(working_dir, console_fontsize,
                                             edit_area_fontsize, bg_color,
                                             font_color)

        # The server format is "name: url:port". We only need "name"
        server = self.combo.getSelectedItem().split(':')[0]
        self.controller.update_config(validated[0], server,
                                      validated[1], validated[2],
                                      validated[3], int(validated[4]))

        # If no values have been changed, print that settings have been
        # updated without errors
        if validated[5]:
            self.logger.info("Settings have been successfully updated.")

        # On saving settings, update the console and edit area properties
        self.controller.refreshConsole()
        self.controller.refreshEditArea()
        # Close window
        self.dispose()

        # Refresh the syntax highlighting in a separate thread so it updates
        # after everything else has been done.
        runSwingLater(self.controller.controller.initHighlighting)

    def browse(self, event=None):
        '''
        Open new dialog for the user to select a path as default working dir.
        '''
        default_path = self.wd_field.getText()
        if not os.path.isdir(default_path):
            default_path = os.getcwd()
        fileChooser = JFileChooser(default_path)
        fileChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)
        # Fixed showDialog bug using showOpenDialog instead. The former was
        # duplicating the last folder name in the path due to a Java bug in
        # OSX in the implementation of JFileChooser!
        status = fileChooser.showOpenDialog(self)
        if status == JFileChooser.APPROVE_OPTION:
            self.wd_field.setText(fileChooser.getSelectedFile().toString())
