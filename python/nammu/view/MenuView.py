'''
Created on 15 Apr 2015

Initializes the menu view and sets its layout.

@author: raquel-ucl
'''

from javax.swing import JMenuBar, JMenu, JMenuItem, ImageIcon
from java.awt.event import KeyEvent

class MenuView(JMenuBar):
    
    def __init__(self):
        print "I'm the menu view"
        #self.controller = MenuController
        
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
        
    def onOpenFileSelect(self, event):
        print "Browse for new file to open and load it in text area."
            
    def onSaveFileSelect(self, event):
        print "Browse for place to save current file."
            
    def onCloseFileSelect(self, event):
        print "Prompt save current, close it and clean text area."
            
    def onQuitFileSelect(self, event):
            print "Prompt save current, exit Nammu."
       
       