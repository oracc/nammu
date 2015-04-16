'''
Created on 15 Apr 2015

Initializes the menu view and sets its layout.

@author: raquel-ucl
'''

from javax.swing import JMenuBar, JMenu, JMenuItem, ImageIcon, JFileChooser
from javax.swing.filechooser import FileNameExtensionFilter
from java.awt.event import KeyEvent

class MenuView(JMenuBar):
    
    def __init__(self, controller):
        print "I'm the menu view"
        
        #Save reference to controller to handle events
        self.controller = controller
        
        fileMenu = JMenu("File")
        fileMenu.setMnemonic(KeyEvent.VK_F)
        
        icon = ImageIcon("../../../resources/images/new.png")
        newFileMenuItem = JMenuItem("New", icon, actionPerformed=self.onNewFileSelect)
        newFileMenuItem.setMnemonic(KeyEvent.VK_N)
        newFileMenuItem.setToolTipText("Creates empty ATF file for edition")
        
        icon = ImageIcon("../../../resources/images/open.png")
        openFileMenuItem = JMenuItem("Open", icon, actionPerformed=self.onOpenFileSelect)
        openFileMenuItem.setMnemonic(KeyEvent.VK_O)
        openFileMenuItem.setToolTipText("Opens ATF file for edition")
        
        icon = ImageIcon("../../../resources/images/save.png")
        saveFileMenuItem = JMenuItem("Save", icon, actionPerformed=self.onSaveFileSelect)
        saveFileMenuItem.setMnemonic(KeyEvent.VK_S)
        saveFileMenuItem.setToolTipText("Saves current file")
         
        icon = ImageIcon("../../../resources/images/close.png")
        closeFileMenuItem = JMenuItem("Close", icon, actionPerformed=self.onCloseFileSelect)
        closeFileMenuItem.setMnemonic(KeyEvent.VK_C)
        closeFileMenuItem.setToolTipText("Close current file")
        
        icon = ImageIcon("../../../resources/images/quit.png")
        quitFileMenuItem = JMenuItem("Quit", icon, actionPerformed=self.onQuitFileSelect)
        quitFileMenuItem.setMnemonic(KeyEvent.VK_Q)
        quitFileMenuItem.setToolTipText("Exit application")
        
        fileMenu.add(newFileMenuItem)
        fileMenu.add(openFileMenuItem)
        fileMenu.add(saveFileMenuItem)
        fileMenu.add(closeFileMenuItem)
        fileMenu.addSeparator()
        fileMenu.add(quitFileMenuItem)
                
        self.add(fileMenu)
        
        
        
        editMenu = JMenu("Edit")
        editMenu.setMnemonic(KeyEvent.VK_E)
        
        icon = ImageIcon("../../../resources/images/undo.png")
        undoMenuItem = JMenuItem("Undo", icon, actionPerformed=self.onUndoSelect)
        undoMenuItem.setMnemonic(KeyEvent.VK_U)
        undoMenuItem.setToolTipText("Undo last action")
        
        icon = ImageIcon("../../../resources/images/redo.png")
        redoMenuItem = JMenuItem("Redo", icon, actionPerformed=self.onRedoSelect)
        redoMenuItem.setMnemonic(KeyEvent.VK_R)
        redoMenuItem.setToolTipText("Redo last undone action")
        
        icon = ImageIcon("../../../resources/images/copy.png")
        copyMenuItem = JMenuItem("Copy", icon, actionPerformed=self.onCopySelect)
        copyMenuItem.setMnemonic(KeyEvent.VK_Y)
        copyMenuItem.setToolTipText("Copy text selection")
        
        icon = ImageIcon("../../../resources/images/cut.png")
        cutMenuItem = JMenuItem("Cut", icon, actionPerformed=self.onCutSelect)
        cutMenuItem.setMnemonic(KeyEvent.VK_X)
        cutMenuItem.setToolTipText("Cut text selection")
         
        icon = ImageIcon("../../../resources/images/paste.png")
        pasteMenuItem = JMenuItem("Paste", icon, actionPerformed=self.onPasteSelect)
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
        
        icon = ImageIcon("../../../resources/images/validate.png")
        validateMenuItem = JMenuItem("Validate ATF", icon, actionPerformed=self.onValidateSelect)
        validateMenuItem.setMnemonic(KeyEvent.VK_V)
        validateMenuItem.setToolTipText("Check current ATF correctness")
        
        icon = ImageIcon("../../../resources/images/lematise.png")
        lemmatiseMenuItem = JMenuItem("Lemmatise ATF", icon, actionPerformed=self.onLemmatiseSelect)
        lemmatiseMenuItem.setMnemonic(KeyEvent.VK_L)
        lemmatiseMenuItem.setToolTipText("Obtain lemmas for current ATF text")
                
        atfMenu.add(validateMenuItem)
        atfMenu.add(lemmatiseMenuItem)
        
        self.add(atfMenu)
        
        
                
        
        windowMenu = JMenu("Window")
        windowMenu.setMnemonic(KeyEvent.VK_A)
        
        icon = ImageIcon("../../../resources/images/model.png")
        modelMenuItem = JMenuItem("Model View", icon, actionPerformed=self.onModelSelect)
        modelMenuItem.setMnemonic(KeyEvent.VK_M)
        modelMenuItem.setToolTipText("Change to ATF data model view")
        
        icon = ImageIcon("../../../resources/images/console.png")
        consoleMenuItem = JMenuItem("View/Hide Console", icon, actionPerformed=self.onConsoleSelect)
        consoleMenuItem.setMnemonic(KeyEvent.VK_N)
        consoleMenuItem.setToolTipText("View/Hide Console")
        
        icon = ImageIcon("../../../resources/images/toolbar.png")
        toolbarMenuItem = JMenuItem("View/Hide Toolbar", icon, actionPerformed=self.onToolbarSelect)
        toolbarMenuItem.setMnemonic(KeyEvent.VK_T)
        toolbarMenuItem.setToolTipText("View/Hide Toolbar")
        
        icon = ImageIcon("../../../resources/images/unicode.png")
        unicodeMenuItem = JMenuItem("Unicode Keyboard", icon, actionPerformed=self.onUnicodeSelect)
        unicodeMenuItem.setMnemonic(KeyEvent.VK_Z)
        unicodeMenuItem.setToolTipText("Use Unicode characters")
                
        windowMenu.add(modelMenuItem)
        windowMenu.add(consoleMenuItem)
        windowMenu.add(toolbarMenuItem)
        windowMenu.add(unicodeMenuItem)
        
        self.add(windowMenu)
        
        
        helpMenu = JMenu("Help")
        helpMenu.setMnemonic(KeyEvent.VK_A)
        
        icon = ImageIcon("../../../resources/images/help.png")
        helpMenuItem = JMenuItem("Help", icon, actionPerformed=self.onHelpSelect)
        helpMenuItem.setMnemonic(KeyEvent.VK_H)
        helpMenuItem.setToolTipText("Displays ATF documentation")
        
        icon = ImageIcon("../../../resources/images/about.png")
        aboutMenuItem = JMenuItem("About", icon, actionPerformed=self.onAboutSelect)
        aboutMenuItem.setMnemonic(KeyEvent.VK_B)
        aboutMenuItem.setToolTipText("Displays information about Nammu")
                
        helpMenu.add(helpMenuItem)
        helpMenu.addSeparator()
        helpMenu.add(aboutMenuItem)
        
        self.add(helpMenu)
        
        
        #self.add(JMenu("Edit"))
        #Suboptions: Undo, Redo | Copy, Cut, Paste
        
        #self.add(JMenu("ATF"))
        #Suboptions: Validate, Lemmatize 
        
        #self.add(JMenu("Window"))
        #Suboptions: View/Hide Console |  Model View / Text View | Toggle Unicode Keyboard
        
        #self.add(JMenu("Help"))
        #Suboptions: Help | About
        
    def onNewFileSelect(self, event):
        print "Prompt save current, close it and clean text area."
        self.controller.newFile()
        
    def onOpenFileSelect(self, event):
        print "Browse for new file to open and load it in text area."
        self.controller.openFile()
        
#         chooseFile = JFileChooser()
#         filter = FileNameExtensionFilter("ATF files", ["atf"])
#         chooseFile.addChoosableFileFilter(filter)
# 
#         returnedValue = chooseFile.showDialog(self.panel, "Choose file")
# 
#         if returnedValue == JFileChooser.APPROVE_OPTION:
#             atfFile = chooseFile.getSelectedFile()
#             atfText = self.readFile(atfFile)
#             return text()
# 
# 
#     def readFile(self, file):
#         filename = file.getCanonicalPath()
#         f = open(filename, "r")
#         text = f.read()
#         return text
#         
#            def actionPerformed(self, e):
#      retval = self.outer._fileChooser.showOpenDialog(self.outer)
#      if retval==JFileChooser.APPROVE_OPTION:
#        f = self.outer._fileChooser.getSelectedFile()
#        try:
#          reader = FileReader(f)
#          self.outer._editArea.read(reader, "")  # Use TextComponent read
#        except IOException,ioex:
#          System.out.println(e);
#          System.exit(1);
            
    def onSaveFileSelect(self, event):
        print "Browse for place to save current file."
        self.controller.saveFile()
        
#             retval = self.outer._fileChooser.showSaveDialog(self.outer)
#     if retval == JFileChooser.APPROVE_OPTION:
#       f = self.outer._fileChooser.getSelectedFile()
#       try:
#         writer = FileWriter(f)
#         self.outer._editArea.write(writer)  # TextComponent write
#       except IOException,ioex:
#         JOptionPane.showMessageDialog(self.outer, ioex)
#         System.exit(1)

            
    #Delegate all events to view controller
    def onCloseFileSelect(self, event):
        print "Prompt save current, close it and clean text area."
        self.controller.closeFile()
            
    def onQuitFileSelect(self, event):
        print "Prompt save current, exit Nammu."
        self.controller.quit()
            
    def onUndoSelect(self, event):
        print "Undo last change." 
        self.controller.undo()
        
    def onRedoSelect(self, event):
        print "Redo last undone action."
        self.controller.redo()
        
    def onCopySelect(self, event):
        print "Copy selected text."
        self.controller.copy()
       
    def onCutSelect(self, event):
        print "Cut selected text."
        self.controller.cut()
    
    def onPasteSelect(self, event):
        print "Paste clipboard text."
        self.controller.paste()
        
    def onValidateSelect(self, event):
        print "Validate ATF."
        self.controller.validate("text area content or path to file?")
    
    def onLemmatiseSelect(self, event):
        print "Lemmatise ATF."
        self.controller.lemmatise("text area content or path to file?")
        
    def onHelpSelect(self, event):
        print "Display ATF help."
        self.controller.showHelp()
        
    def onAboutSelect(self, event):
        print "Display Nammu information." 
        self.controller.showAbout() 
       
    def onModelSelect(self, event):
        print "Change to model view."
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
        
               