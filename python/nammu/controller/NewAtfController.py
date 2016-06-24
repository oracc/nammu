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

from ..utils import get_yaml_config
from ..view.NewAtfView import NewAtfView


class NewAtfController:
    def __init__(self, maincontroller):
        self.controller = maincontroller
        config = get_yaml_config('settings.yaml')
        self.projects = config['projects']
        self.languages = config['languages']
        self.protocols = config['protocols']
        self.template = ''
        self.view = NewAtfView(self,
                               self.projects,
                               self.languages,
                               self.protocols)
        self.view.display()

    def set_template(self):
        self.controller.atfAreaController.setAtfAreaText(self.template)
