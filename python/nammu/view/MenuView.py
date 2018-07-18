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

import collections
from .Menu import Menu
from javax.swing import JMenuBar
from java.awt.event import KeyEvent


class MenuView(JMenuBar):
    '''
    Initializes the menu view and sets its layout.
    '''
    def __init__(self, controller):
        # Save reference to controller to handle events
        self.controller = controller

        # TODO Refactor to avoid duplication - See issue#16
        # https://github.com/UCL-RITS/nammu/issues/16

        # Create dictionaries for the menus and the menu items
        # with corresponding key event and related method name
        # Note these need to be added to the menu in a certain order,
        # so dict random order can be changed to element addition order
        # with collections.OrderedDict and then adding the elements
        # one by one. If all are added at the same time, there's no
        # guarantee of order.
        menus = {}
        menus = collections.OrderedDict()
        menus['File'] = KeyEvent.VK_F
        menus['Edit'] = KeyEvent.VK_E
        menus['ATF'] = KeyEvent.VK_A
        menus['Window'] = KeyEvent.VK_W
        menus['Help'] = KeyEvent.VK_H

        menuItems = {}

        menuItems["File"] = {}
        menuItems["File"] = collections.OrderedDict()
        menuItems["File"]["New"] = [KeyEvent.VK_N, "newFile"]
        menuItems["File"]["Open"] = [KeyEvent.VK_O, "openFile"]
        menuItems["File"]["Save"] = [KeyEvent.VK_S, "saveFile"]
        menuItems["File"]["Save As..."] = [KeyEvent.VK_A, "saveAsFile"]
        menuItems["File"]["Close"] = [KeyEvent.VK_W, "closeFile"]
        menuItems["File"]["Print"] = [KeyEvent.VK_P, "printFile"]
        menuItems["File"]["Quit"] = [KeyEvent.VK_Q, "quit"]

        menuItems["Edit"] = {}
        menuItems["Edit"] = collections.OrderedDict()
        menuItems["Edit"]["Undo"] = [KeyEvent.VK_Z, "undo"]
        menuItems["Edit"]["Redo"] = [KeyEvent.VK_R, "redo"]
        menuItems["Edit"]["Copy"] = [KeyEvent.VK_C, "copy"]
        menuItems["Edit"]["Cut"] = [KeyEvent.VK_X, "cut"]
        menuItems["Edit"]["Paste"] = [KeyEvent.VK_V, "paste"]
        menuItems["Edit"]["Find/Replace"] = [KeyEvent.VK_G, "find"]
        menuItems["Edit"]["Settings"] = [KeyEvent.VK_E, "editSettings"]

        menuItems["ATF"] = {}
        menuItems["ATF"] = collections.OrderedDict()
        menuItems["ATF"]["Validate"] = [KeyEvent.VK_D, "validate"]
        menuItems["ATF"]["Lemmatise"] = [KeyEvent.VK_L, "lemmatise"]

        menuItems["Window"] = {}
        menuItems["Window"] = collections.OrderedDict()
        menuItems["Window"]["Display Model View"] = [KeyEvent.VK_M,
                                                     "displayModelView"]
        menuItems["Window"]["View/Hide Console"] = [KeyEvent.VK_B, "console"]
        menuItems["Window"]["View/Hide Toolbar"] = [KeyEvent.VK_T, "toolbar"]
        menuItems["Window"]["Toggle Vertical Split Editor"] = [
                                                            KeyEvent.VK_COMMA,
                                                            "splitEditorV"
                                                            ]
        menuItems["Window"]["Toggle Horizonal Split Editor"] = [
                                                            KeyEvent.VK_PERIOD,
                                                            "splitEditorH"
                                                            ]
        menuItems["Window"]["Toggle Arabic Translation Editor"] = [
                                                                KeyEvent.VK_K,
                                                                "arabic"
                                                                ]

        menuItems["Help"] = {}
        menuItems["Help"] = collections.OrderedDict()
        menuItems["Help"]["Help"] = [KeyEvent.VK_H, "showHelp"]
        menuItems["Help"]["About"] = [KeyEvent.VK_A, "showAbout"]

        # Menu Items after which there is a menu separator
        separators = {"File": ["Close", "Print"],
                      "Edit": ["Redo", "Paste", "Find/Replace"],
                      "ATF": [],
                      "Window": ["Display Model View"],
                      "Help": ["Help"]}

        # Create menu items and add to menu bar
        for menuName, keyEvent in menus.items():
            menu = Menu(self,
                        menuName,
                        keyEvent,
                        menuItems[menuName],
                        separators[menuName])
            self.add(menu)

    # Delegate methods not found here to view controller
    def __getattr__(self, name):
        return getattr(self.controller, name)
