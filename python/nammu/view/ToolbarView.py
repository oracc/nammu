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

        #Give reference to controller to delegate action response
        self.controller = controller

        #Build Toolbar following schema in issue#18 and mockups in
        #https://github.com/UCL-RITS/nammu/tree/master/doc/mockups
        #https://github.com/UCL-RITS/nammu/issues/18

        #TODO Refactor to avoid duplication - See issue#16
        #https://github.com/UCL-RITS/nammu/issues/16

        options = ['NewFile', 'OpenFile', 'SaveFile', 'CloseFile', 'PrintFile', 'Undo', 'Redo',
                  'Copy', 'Cut', 'Paste', 'Validate', 'Lemmatise', 'Unicode',
                  'Console', 'DisplayModelView', 'EditSettings', 'ShowHelp', 'ShowAbout', 'Quit']
        methods = {}
        methods = collections.OrderedDict()
        for option in options:
            methods[option] = "on" + option + "Click"
            print methods[option]

        tooltips = {'NewFile': 'Creates empty ATF file for edition',
                 'OpenFile': 'Opens ATF file for edition',
                 'SaveFile': 'Saves current file',
                 'CloseFile': 'Closes current file',
                 'PrintFile': 'Prints current file',
                 'Undo': 'Undo last action',
                 'Redo': 'Redo last undone action',
                 'Copy': 'Copy text selection',
                 'Cut': 'Cut text selection',
                 'Paste': 'Paste clipboard content',
                 'Validate': 'Check current ATF correctness',
                 'Lemmatise': 'Obtain lemmas for current ATF text',
                 'Unicode': 'Use Unicode characters',
                 'Console': 'View/Hide Console',
                 'DisplayModelView': 'Change to ATF data model view',
                 'EditSettings': 'Change Nammu settings',
                 'ShowHelp': 'Displays ATF documentation',
                 'ShowAbout': 'Displays information about Nammu and ORACC',
                 'Quit': 'Exits Nammu'}

        for name, method in methods.items():
            icon = ImageIcon(self.findImageResource(name))
#            button = JButton(icon, actionperformed = getattr(self, options[0].lower() + options[1:]))
            button = JButton(icon, actionPerformed = getattr(self, "newFile"))
            button.setToolTipText(tooltips[name])
            self.add(button)
            #Work out is separator is needed
            if name in ['PrintFile', 'Redo', 'Paste', 'Lemmatise', 'Unicode',
                        'Console', 'DisplayModelView', 'ShowAbout']:
                self.addSeparator()

    def __getattr__(self, name):
        return getattr(self.controller, name)

    def findImageResource(self, name):
        #Create helper object to load icon images in jar
        loader = ClassLoader.getSystemClassLoader()
        #Load image
        return loader.getResource("resources/images/" + name.lower() + ".png")




