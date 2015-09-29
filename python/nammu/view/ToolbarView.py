'''
Created on 15 Apr 2015

Initializes the toolbar view and sets its layout.

@author: raquel-ucl
'''

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
        
        methods = {'new': 'onNewFileClick', 
                 'open': 'onOpenFileClick',
                 'save': 'onSaveFileClick', 
                 'close': 'onCloseFileClick', 
                 'print': 'onPrintFileClick', 
                 'undo': 'onUndoClick', 
                 'redo': 'onRedoClick', 
                 'copy': 'onCopyClick', 
                 'cut': 'onCutClick', 
                 'paste': 'onPasteClick', 
                 'validate': 'onValidateClick', 
                 'lemmatise': 'onLemmatiseClick', 
                 'unicode': 'onUnicodeClick',
                 'console': 'onConsoleClick', 
                 'model': 'onModelClick', 
                 'settings': 'onSettingsClick', 
                 'help': 'onHelpClick', 
                 'about': 'onAboutClick', 
                 'quit': 'onQuitClick'}
        
        tooltips = {'new': 'Creates empty ATF file for edition', 
                 'open': 'Opens ATF file for edition',
                 'save': 'Saves current file', 
                 'close': 'Closes current file', 
                 'print': 'Prints current file', 
                 'undo': 'Undo last action', 
                 'redo': 'Redo last undone action', 
                 'copy': 'Copy text selection', 
                 'cut': 'Cut text selection', 
                 'paste': 'Paste clipboard content', 
                 'validate': 'Check current ATF correctness', 
                 'lemmatise': 'Obtain lemmas for current ATF text', 
                 'unicode': 'Use Unicode characters',
                 'console': 'View/Hide Console', 
                 'model': 'Change to ATF data model view', 
                 'settings': 'Change Nammu settings', 
                 'help': 'Displays ATF documentation', 
                 'about': 'Displays information about Nammu and ORACC', 
                 'quit': 'Exits Nammu'}
        
        for name, method in methods.iteritems():
            icon = ImageIcon(findImageResource(name))
            button = JButton(icon, actionPerformed=getattr(self, method))
            button.setToolTipText(tooltips[name])
            self.add(button)
            #Work out is separator is needed
            if name in ['print', 'redo', 'paste', 'lemmatise', 'unicode', 
                        'console', 'model', 'about']:
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

    def findImageResource(name):
        #Create helper object to load icon images in jar
        loader = ClassLoader.getSystemClassLoader()
        #Load image
        loader.getResource("resources/images"+name+".png")

  
        
        