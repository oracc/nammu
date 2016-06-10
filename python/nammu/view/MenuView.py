'''
Created on 15 Apr 2015

Initializes the menu view and sets its layout.

@author: raquel-ucl
'''

import collections
from .Menu import Menu
from javax.swing import JMenuBar
from java.awt.event import KeyEvent


class MenuView(JMenuBar):

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
        menuItems["Window"]["Unicode Keyboard"] = [KeyEvent.VK_K, "unicode"]

        menuItems["Help"] = {}
        menuItems["Help"] = collections.OrderedDict()
        menuItems["Help"]["Settings"] = [KeyEvent.VK_E, "editSettings"]
        menuItems["Help"]["Help"] = [KeyEvent.VK_H, "showHelp"]
        menuItems["Help"]["About"] = [KeyEvent.VK_A, "showAbout"]

        # Menu Items after which there is a menu separator
        separators = {"File": ["Close", "Print"],
                      "Edit": ["Redo"],
                      "ATF": [],
                      "Window": ["Display Model View"],
                      "Help": ["Settings", "Help"]}

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
