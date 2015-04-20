'''
Created on 15 Apr 2015

Initializes the menu view and sets its layout.

@author: raquel-ucl
'''

from javax.swing import JMenuBar, JMenu, JMenuItem, ImageIcon
from java.awt.event import KeyEvent

class MenuView(JMenuBar):
    
    def __init__(self, controller):
        print "I'm the menu view"
        
        #Save reference to controller to handle events
        self.controller = controller
        
        #Build Menu as per issue#18 
        #See https://github.com/UCL-RITS/nammu/issues/18
        
        #TODO Refactor to avoid duplication - See issue#16 
        #https://github.com/UCL-RITS/nammu/issues/16
        
        fileMenu = JMenu("File")
        fileMenu.setMnemonic(KeyEvent.VK_F)
        
        newFileMenuItem = JMenuItem("New", actionPerformed=self.onNewFileSelect)
        newFileMenuItem.setMnemonic(KeyEvent.VK_N)
        
        openFileMenuItem = JMenuItem("Open", actionPerformed=self.onOpenFileSelect)
        openFileMenuItem.setMnemonic(KeyEvent.VK_O)
    
        saveFileMenuItem = JMenuItem("Save", actionPerformed=self.onSaveFileSelect)
        saveFileMenuItem.setMnemonic(KeyEvent.VK_S)
         
        closeFileMenuItem = JMenuItem("Close", actionPerformed=self.onCloseFileSelect)
        closeFileMenuItem.setMnemonic(KeyEvent.VK_C)
        
        printFileMenuItem = JMenuItem("Print", actionPerformed=self.onPrintFileSelect)
        printFileMenuItem.setMnemonic(KeyEvent.VK_P)
        
        quitFileMenuItem = JMenuItem("Quit", actionPerformed=self.onQuitFileSelect)
        quitFileMenuItem.setMnemonic(KeyEvent.VK_Q)

        
        fileMenu.add(newFileMenuItem)
        fileMenu.add(openFileMenuItem)
        fileMenu.add(saveFileMenuItem)
        fileMenu.add(closeFileMenuItem)
        fileMenu.addSeparator()
        fileMenu.add(printFileMenuItem)
        fileMenu.addSeparator()
        fileMenu.add(quitFileMenuItem)
                
        self.add(fileMenu)
        
        editMenu = JMenu("Edit")
        editMenu.setMnemonic(KeyEvent.VK_E)
        
        undoMenuItem = JMenuItem("Undo", actionPerformed=self.onUndoSelect)
        undoMenuItem.setMnemonic(KeyEvent.VK_U)
        
        redoMenuItem = JMenuItem("Redo", actionPerformed=self.onRedoSelect)
        redoMenuItem.setMnemonic(KeyEvent.VK_R)
        
        copyMenuItem = JMenuItem("Copy", actionPerformed=self.onCopySelect)
        copyMenuItem.setMnemonic(KeyEvent.VK_Y)
        
        cutMenuItem = JMenuItem("Cut", actionPerformed=self.onCutSelect)
        cutMenuItem.setMnemonic(KeyEvent.VK_X)
         
        pasteMenuItem = JMenuItem("Paste", actionPerformed=self.onPasteSelect)
        pasteMenuItem.setMnemonic(KeyEvent.VK_P)
        pasteMenuItem.setToolTipText("Paste clipboard content")
                
        editMenu.add(undoMenuItem)
        editMenu.add(redoMenuItem)
        editMenu.addSeparator()
        editMenu.add(copyMenuItem)
        editMenu.add(cutMenuItem)
        editMenu.add(pasteMenuItem)
                
        self.add(editMenu)
        
        atfMenu = JMenu("ATF")
        atfMenu.setMnemonic(KeyEvent.VK_A)
        
        validateMenuItem = JMenuItem("Validate ATF", actionPerformed=self.onValidateSelect)
        validateMenuItem.setMnemonic(KeyEvent.VK_V)
        validateMenuItem.setToolTipText("Check current ATF correctness")
        
        lemmatiseMenuItem = JMenuItem("Lemmatise ATF", actionPerformed=self.onLemmatiseSelect)
        lemmatiseMenuItem.setMnemonic(KeyEvent.VK_L)
                
        atfMenu.add(validateMenuItem)
        atfMenu.add(lemmatiseMenuItem)
        
        self.add(atfMenu)
        
        windowMenu = JMenu("Window")
        windowMenu.setMnemonic(KeyEvent.VK_A)
        
        modelMenuItem = JMenuItem("Model View", actionPerformed=self.onModelSelect)
        modelMenuItem.setMnemonic(KeyEvent.VK_M)
        
        consoleMenuItem = JMenuItem("View/Hide Console", actionPerformed=self.onConsoleSelect)
        consoleMenuItem.setMnemonic(KeyEvent.VK_N)
        
        toolbarMenuItem = JMenuItem("View/Hide Toolbar", actionPerformed=self.onToolbarSelect)
        toolbarMenuItem.setMnemonic(KeyEvent.VK_T)
        toolbarMenuItem.setToolTipText("View/Hide Toolbar")
        
        unicodeMenuItem = JMenuItem("Unicode Keyboard", actionPerformed=self.onUnicodeSelect)
        unicodeMenuItem.setMnemonic(KeyEvent.VK_Z)
                
        windowMenu.add(modelMenuItem)
        windowMenu.add(consoleMenuItem)
        windowMenu.add(toolbarMenuItem)
        windowMenu.add(unicodeMenuItem)
        
        self.add(windowMenu)
        
        helpMenu = JMenu("Help")
        helpMenu.setMnemonic(KeyEvent.VK_A)
        
        settingsMenuItem = JMenuItem("Settings...", actionPerformed=self.onSettingsSelect)
        settingsMenuItem.setMnemonic(KeyEvent.VK_H)
        
        helpMenuItem = JMenuItem("Help", actionPerformed=self.onHelpSelect)
        helpMenuItem.setMnemonic(KeyEvent.VK_H)
        
        aboutMenuItem = JMenuItem("About", actionPerformed=self.onAboutSelect)
        aboutMenuItem.setMnemonic(KeyEvent.VK_B)
             
        helpMenu.add(settingsMenuItem)
        helpMenu.addSeparator()   
        helpMenu.add(helpMenuItem)
        helpMenu.addSeparator()
        helpMenu.add(aboutMenuItem)
        
        self.add(helpMenu)
        
    #Delegate all events to view controller
        
    def onNewFileSelect(self, event):
        self.controller.newFile()
        
    def onOpenFileSelect(self, event):
        self.controller.openFile()
    
    def onSaveFileSelect(self, event):
        self.controller.saveFile()
        
    def onCloseFileSelect(self, event):
        self.controller.closeFile()
            
    def onPrintFileSelect(self, event):
        self.controller.printFile()
        
    def onQuitFileSelect(self, event):
        self.controller.quit()
            
    def onUndoSelect(self, event):
        self.controller.undo()
        
    def onRedoSelect(self, event):
        self.controller.redo()
        
    def onCopySelect(self, event):
        self.controller.copy()
       
    def onCutSelect(self, event):
        self.controller.cut()
    
    def onPasteSelect(self, event):
        self.controller.paste()
        
    def onValidateSelect(self, event):
        self.controller.validate("text area content or path to file?")
    
    def onLemmatiseSelect(self, event):
        self.controller.lemmatise("text area content or path to file?")
        
    def onSettingsSelect(self, event):
        print "Edit Nammu settings."
        self.controller.editSettings()
        
    def onHelpSelect(self, event):
        print "Display ATF help."
        self.controller.showHelp()
        
    def onAboutSelect(self, event):
        print "Display Nammu information." 
        self.controller.showAbout() 
       
    def onModelSelect(self, event):
        self.controller.displayModelView()
        
    def onConsoleSelect(self, event):
        print "Toggle/Display console panel."
        #TODO
        #self.controller.hideConsole()
        #self.controller.displayConsole()
        
    def onToolbarSelect(self, event):
        print "Display/Hide toolbar."
        #TODO
        #self.controller.hideToolbar()
        #self.controller.displayToolbar()
        
    def onUnicodeSelect(self, event):
        print "Use Unicode keyboard."
        #TODO
        #self.controller.unicode(true)
        #self.controller.unicode(false)
        
               