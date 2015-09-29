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
        
        #Create helper object to load icon images in jar
        loader = ClassLoader.getSystemClassLoader()
        
        newIcon = ImageIcon(loader.getResource("resources/images/new.png"))
        newFileButton = JButton(newIcon, 
                                actionPerformed=self.onNewFileClick)
        newFileButton.setToolTipText("Creates empty ATF file for edition")
        self.add(newFileButton)
        
        openIcon = ImageIcon(findImageResource('open'))  
        openFileButton = JButton(openIcon, 
                                 actionPerformed=self.onOpenFileClick)
        openFileButton.setToolTipText("Opens ATF file for edition")
        self.add(openFileButton)
        
        saveIcon = ImageIcon(findImageResource('save'))  
        saveFileButton = JButton(saveIcon, 
                                 actionPerformed=self.onSaveFileClick)
        
        saveFileButton.setToolTipText("Saves current file")
        self.add(saveFileButton)
        
        closeIcon = ImageIcon(findImageResource('close'))  
        closeFileButton = JButton(closeIcon, 
                                  actionPerformed=self.onCloseFileClick)
        closeFileButton.setToolTipText("Close current file")
        self.add(closeFileButton)
        
        printIcon = ImageIcon(findImageResource('print'))  
        printFileButton = JButton(printIcon, 
                                  actionPerformed=self.onPrintFileClick)
        printFileButton.setToolTipText("Close current file")
        self.add(printFileButton)

        #AddSeparator might need addSeparator(Dimension(20,20)) to be visible
        self.addSeparator()

        undoIcon = ImageIcon(findImageResource('undo'))  
        undoButton = JButton(undoIcon, 
                             actionPerformed=self.onUndoClick)
        
        undoButton.setToolTipText("Undo last action")
        self.add(undoButton)
        
        redoIcon = ImageIcon(findImageResource('redo'))  
        redoButton = JButton(redoIcon, 
                             actionPerformed=self.onRedoClick)
        redoButton.setToolTipText("Redo last undone action")
        self.add(redoButton)
        
        #AddSeparator might need addSeparator(Dimension(20,20)) to be visible
        self.addSeparator()
        
        copyIcon = ImageIcon(findImageResource('copy'))  
        copyButton = JButton(copyIcon, 
                             actionPerformed=self.onCopyClick)
        copyButton.setToolTipText("Copy text selection")
        self.add(copyButton)
        
        cutIcon = ImageIcon(findImageResource('cut'))  
        cutButton = JButton(cutIcon, 
                             actionPerformed=self.onCutClick)
        cutButton.setToolTipText("Cut text selection")
        self.add(cutButton)
        
        pasteIcon = ImageIcon(findImageResource('paste'))  
        pasteButton = JButton(pasteIcon, 
                             actionPerformed=self.onPasteClick)
        pasteButton.setToolTipText("Paste clipboard content")
        self.add(pasteButton)
    
        #AddSeparator might need addSeparator(Dimension(20,20)) to be visible
        self.addSeparator()

        validateIcon = ImageIcon(findImageResource('validate'))  
        validateButton = JButton(validateIcon, 
                             actionPerformed=self.onValidateClick)
        validateButton.setToolTipText("Check current ATF correctness")
        self.add(validateButton)
        
        lemmatiseIcon = ImageIcon(findImageResource('lemmatise'))  
        lemmatiseButton = JButton(lemmatiseIcon, 
                             actionPerformed=self.onLemmatiseClick)
        lemmatiseButton.setToolTipText("Obtain lemmas for current ATF text")
        self.add(lemmatiseButton)
        
        #AddSeparator might need addSeparator(Dimension(20,20)) to be visible
        self.addSeparator()
        
        unicodeIcon = ImageIcon(findImageResource('unicode'))  
        unicodeButton = JButton(unicodeIcon, 
                             actionPerformed=self.onUnicodeClick)
        unicodeButton.setToolTipText("Use Unicode characters")
        self.add(unicodeButton)
        
        #AddSeparator might need addSeparator(Dimension(20,20)) to be visible
        self.addSeparator()
        
        consoleIcon = ImageIcon(findImageResource('console'))  
        consoleButton = JButton(consoleIcon, 
                             actionPerformed=self.onConsoleClick)
        consoleButton.setToolTipText("View/Hide Console")
        self.add(consoleButton)
        
        #AddSeparator might need addSeparator(Dimension(20,20)) to be visible
        self.addSeparator()
        
        modelIcon = ImageIcon(findImageResource('model'))  
        modelButton = JButton(modelIcon, 
                             actionPerformed=self.onModelClick)
        modelButton.setToolTipText("Change to ATF data model view")
        self.add(modelButton)
        
        #AddSeparator might need addSeparator(Dimension(20,20)) to be visible
        self.addSeparator()

        settingsIcon = ImageIcon(findImageResource('settings'))  
        settingsButton = JButton(settingsIcon, 
                             actionPerformed=self.onSettingsClick)
        settingsButton.setToolTipText("Change Nammu settings")
        self.add(settingsButton)
        
        helpIcon = ImageIcon(findImageResource('help'))  
        helpButton = JButton(helpIcon, 
                             actionPerformed=self.onHelpClick)
        helpButton.setToolTipText("Displays ATF documentation")
        self.add(helpButton)
        
        aboutIcon = ImageIcon(findImageResource('about'))  
        aboutButton = JButton(aboutIcon, 
                             actionPerformed=self.onAboutClick)
        aboutButton.setToolTipText("Displays information about Nammu")
        self.add(aboutButton)

        #AddSeparator might need addSeparator(Dimension(20,20)) to be visible
        self.addSeparator()
        
        quitIcon = ImageIcon(findImageResource('quit'))  
        quitButton = JButton(quitIcon, 
                             actionPerformed=self.onQuitClick)
        quitButton.setToolTipText("Exit Nammu")
        self.add(quitButton)
        
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
        loader.getResource("resources/images"+name+".png")

  
        
        