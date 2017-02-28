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

from ..view.EditSettingsView import EditSettingsView


class EditSettingsController:
    def __init__(self, maincontroller):
        self.controller = maincontroller
        self.load_config()
        self.view = EditSettingsView(self, self.working_dir, self.servers,
                                     self.keystrokes, self.languages,
                                     self.projects)
        self.view.display()

    def load_config(self):
        '''
        The user's config file should containg all necessary information for
        the settings editor.
        '''
        config_keywords = ['working_dir', 'servers', 'keystrokes',
                           'languages', 'projects']
        for keyword in config_keywords:
            try:
                setattr(self, keyword, self.controller.config[keyword])
            except KeyError:
                self.controller.logger.error('%s missing on settings file.',
                                             keyword)
                self.view.display_error(keyword)

    def update_config(self, working_dir=None, servers=None, keystrokes=None,
                      languages=None, projects=None):
        '''
        Update the settings file with the user input.
        '''
        pass
