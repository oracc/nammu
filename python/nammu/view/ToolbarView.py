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

import collections
from javax.swing import JToolBar, ImageIcon, JButton
from ..utils import find_image_resource


class ToolbarView(JToolBar):
    '''
    Initializes the toolbar view and sets its layout.
    '''
    def __init__(self, controller):
        # Give reference to controller to delegate action response
        self.controller = controller

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
        tooltips['newFile'] = 'Creates empty ATF file for editing'
        tooltips['openFile'] = 'Opens ATF file for editing'
        tooltips['saveFile'] = 'Saves current file'
        tooltips['saveAsFile'] = 'Save As...'
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
            icon = ImageIcon(find_image_resource(name))
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
