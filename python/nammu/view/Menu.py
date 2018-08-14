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

from javax.swing import JMenu, JMenuItem


class Menu(JMenu):

    def __init__(self, menuView, name, keyEvent, menuItems, separators):
        self.menuView = menuView
        self.setText(name)
        self.setMnemonic(keyEvent)
        self.items = self.createItems(menuItems)
        for item in self.items:
            self.add(item)
            if item.getText() in separators:
                self.addSeparator()

    def createItems(self, menuItems):
        items = []

        # Refer to MenuView's menuItems dictionary where each menu item has an
        # array of two elements, the first is the key event and the second is
        # the action asigned to the menu item
        def getMethod(name):
            return menuItems[name][1]

        def getKeyEvent(name):
            return menuItems[name][0]

        for name, keyEvent in menuItems.items():
            actionPerformed = getattr(self.menuView.controller,
                                      getMethod(name))
            item = JMenuItem(name, actionPerformed=actionPerformed)
            item.setMnemonic(getKeyEvent(name))
            items.append(item)

        return items
