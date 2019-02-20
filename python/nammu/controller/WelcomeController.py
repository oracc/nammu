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

from ..view.WelcomeView import WelcomeView
from ..utils import save_yaml_config


class WelcomeController:
    def __init__(self, maincontroller):
        self.controller = maincontroller
        self.config = self.controller.config
        self.view = WelcomeView(self)
        self.view.display()

    def update_welcome_flag(self, flag):
        '''
        Method to update the new user flag in the user's config file
        '''
        self.config['new_user'] = flag
        save_yaml_config(self.config)
        self.controller.logger.debug('Settings updated.')
