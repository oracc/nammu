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
        
        options= ['NewFile', 'OpenFile', 'SaveFile', 'CloseFile', 'PrintFile', 'Undo', 'Redo', 
                  'Copy', 'Cut', 'Paste', 'Validate', 'Lemmatise', 'Unicode',
                  'Console', 'Model', 'Settings', 'Help', 'About', 'Quit']    
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
                 'Model': 'Change to ATF data model view', 
                 'Settings': 'Change Nammu settings', 
                 'Help': 'Displays ATF documentation', 
                 'About': 'Displays information about Nammu and ORACC', 
                 'Quit': 'Exits Nammu'}
        
        for name, method in methods.items():
            icon = ImageIcon(self.findImageResource(name))
            button = JButton(icon, actionPerformed=getattr(self, method))
            button.setToolTipText(tooltips[name])
            self.add(button)
            #Work out is separator is needed
            if name in ['PrintFile', 'Redo', 'Paste', 'Lemmatise', 'Unicode', 
                        'Console', 'Model', 'About']:
                self.addSeparator()
        
        
    def onNewFileClick(self, event):
        self.controller.newFile()
        
    def onOpenFileClick(self, event):
        self.controller.openFile()
        
    def onSaveFileClick(self, event):
        self.controller.saveFile()
        
    def onCloseFileClick(self, event):
        self.controller.closeFile()
        
    def onPrintFileClick(self, event):
        self.controller.printFile()
        
    def onUndoClick(self, event):
        self.controller.undo()
        
    def onRedoClick(self, event):
        self.controller.redo()
        
    def onCopyClick(self, event):
        self.controller.copy()
       
    def onCutClick(self, event):
        self.controller.cut()
    
    def onPasteClick(self, event):
        self.controller.paste()
        
    def onValidateClick(self, event):
        self.controller.validate("text area content or path to file?")
        
    def onLemmatiseClick(self, event):    
        self.controller.lemmatise("text area content or path to file?")
        
    def onUnicodeClick(self, event):
        print "Change to Unicode keyboard."   
        #TODO
        #self.controller.unicode(true)
        #self.controller.unicode(false)
        
    def onConsoleClick(self, event):
        print "Toggle console panel."  
        #TODO
        #self.controller.hideConsole()
        #self.controller.displayConsole()
        
    def onModelClick(self, event):
        self.controller.displayModelView()
        
    def onSettingsClick(self, event):
        print "Edit Nammu settings."
        self.controller.editSettings()
        
    def onHelpClick(self, event):
        print "Display ATF help."
        self.controller.showHelp()
        
    def onAboutClick(self, event):
        print "Display Nammu information." 
        self.controller.showAbout() 
    
    def onQuitClick(self, event):
        self.controller.quit()

    def findImageResource(self, name):
        #Create helper object to load icon images in jar
        loader = ClassLoader.getSystemClassLoader()
        #Load image
        return loader.getResource("resources/images/" + name.lower() + ".png")

  
        
        