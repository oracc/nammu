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

from ..view.MenuView import MenuView


class MenuController(object):
    '''
    Creates the menu view and handles menu actions.
    '''
    def __init__(self, mainController):

        # Needs delegating to parent presenter
        # Note: self.controller needs to be defined before creating the
        # ToolbarView, since the ToolbaView will delegate some actions to it.
        self.mainController = mainController

        # Create view with a reference to its controller to handle events
        self.view = MenuView(self)

    # Some actions need to be delegated to NammuController.
    # E.g. actions in menu that'll need modification of text area controlled
    # elsewhere and not accessible from this controller; as opposed to e.g.
    # showHelp that can be dealt with from MenuController.

    # Whenever a MenuController's method is invoked, __getattr__ will search
    # for that given method name in this class. If it's not found, it'll
    # delegate the action with same name to NammuController
    def __getattr__(self, name):
        return getattr(self.mainController, name)
