'''
Created on 15 Apr 2015

Initializes the toolbar view and sets its layout.

@author: raquel-ucl
'''

import collections
from javax.swing import JToolBar, ImageIcon, JButton
from java.lang import ClassLoader


class ToolbarView(JToolBar):

    def __init__(self, controller):
        # Give reference to controller to delegate action response
        self.controller = controller

        # TODO Refactor to avoid duplication - See issue#16
        # https://github.com/UCL-RITS/nammu/issues/16

        # Content needs to be displayed in an orderly fashion so that buttons
        # are placed where we expect them to be, not in the ramdon order dicts
        # have.
        # We also can't create the tooltips dict e.g.:
        # tooltips = { 'a' : 'A', 'b' : 'B', 'c' : 'C' }
        # because it will still be randomly ordered. Elements need to be added
        # to the dict in the order we want them to be placed in the toolbar for
        # OrderedDict to work
        tooltips = {}
        tooltips = collections.OrderedDict()
        tooltips['newFile'] = 'Creates empty ATF file for edition'
        tooltips['openFile'] = 'Opens ATF file for edition'
        tooltips['saveFile'] = 'Saves current file'
        tooltips['closeFile'] = 'Closes current file'
        tooltips['printFile'] = 'Prints current file'
        tooltips['undo'] = 'Undo last action'
        tooltips['redo'] = 'Redo last undone action'
        tooltips['copy'] = 'Copy text selection'
        tooltips['cut'] = 'Cut text selection'
        tooltips['paste'] = 'Paste clipboard content'
        tooltips['validate'] = 'Check current ATF correctness'
        tooltips['lemmatise'] = 'Obtain lemmas for current ATF text'
        tooltips['displayModelView'] = 'Change to ATF data model view'
        tooltips['editSettings'] = 'Change Nammu settings'
        tooltips['showHelp'] = 'Displays ATF documentation'
        tooltips['showAbout'] = 'Displays information about Nammu and ORACC'
        tooltips['quit'] = 'Exits Nammu'

        for name, tooltip in tooltips.items():
            icon = ImageIcon(self.findImageResource(name))
            button = JButton(icon, actionPerformed=getattr(self, name))
            button.setToolTipText(tooltip)
            self.add(button)
            # Work out is separator is needed
            if name in ['printFile', 'redo', 'paste', 'lemmatise', 'unicode',
                        'console', 'displayModelView', 'showAbout']:
                self.addSeparator()

    def __getattr__(self, name):
        return getattr(self.controller, name)

    def validate(self, event=None):
        if event:
            return self.controller.mainController.validate(event)

    def findImageResource(self, name):
        # Create helper object to load icon images in jar
        loader = ClassLoader.getSystemClassLoader()
        # Load image
        return loader.getResource("resources/images/" + name.lower() + ".png")
