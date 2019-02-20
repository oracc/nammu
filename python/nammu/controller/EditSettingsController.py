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

from ..view.EditSettingsView import EditSettingsView
from ..utils import save_yaml_config


class EditSettingsController:
    def __init__(self, maincontroller):
        self.controller = maincontroller
        self.config = self.controller.config
        self.load_config()
        self.view = EditSettingsView(self, self.working_dir, self.servers,
                                     self.console_style, self.edit_area_style,
                                     self.keystrokes, self.languages,
                                     self.projects)
        self.view.display()

    def load_config(self):
        '''
        The user's config file should containg all necessary information for
        this settings editor.
        '''
        config_keywords = ['working_dir', 'servers', 'keystrokes',
                           'languages', 'projects', 'console_style',
                           'edit_area_style']
        for keyword in config_keywords:
            try:
                setattr(self, keyword, self.config[keyword])
            except KeyError:
                self.controller.logger.error('%s missing on settings file.',
                                             keyword)
                self.view.display_error(keyword)

    def update_config(self, working_dir, server, console_fontsize, font_color,
                      background_color, edit_area_fontsize, keystrokes=None,
                      languages=None, projects=None):
        '''
        Update the settings file with the user input.
        '''
        # TODO: As of v0.6, only working_dir and servers are editable from the
        #       settings window. The other tabs for keystrokes, languages and
        #       projects will be added later.
        self.config['working_dir']['default'] = working_dir
        self.config['servers']['default'] = server
        self.config['console_style']['fontsize']['user'] = console_fontsize
        self.config['console_style']['font_color']['user'] = font_color
        self.config[
                'console_style']['background_color']['user'] = background_color
        self.config['edit_area_style']['fontsize']['user'] = edit_area_fontsize
        self.controller.logger.debug("Settings updated.")
        save_yaml_config(self.config)

    def refreshConsole(self):
        self.controller.consoleController.refreshConsole()

    def refreshEditArea(self):
        self.controller.atfAreaController.refreshEditArea()
