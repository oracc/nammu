'''
Created on 15 Apr 2015

Initializes the toolbar view and sets its layout.

@author: raquel-ucl
'''

from javax.swing import JToolBar, ImageIcon, JButton

class ToolbarView(JToolBar):
    
    def __init__(self, controller):
        print "I'm the toolbar view"
        
        #Give reference to controller to delegate action response
        self.controller = controller
        
        newIcon = ImageIcon("../../../resources/images/new.png")
        newFileButton = JButton("New", newIcon, 
                                actionPerformed=self.onNewFileClick)
        self.add(newFileButton)
        
        openIcon = ImageIcon("../../../resources/images/open.png")
        openFileButton = JButton("Open", openIcon, 
                                 actionPerformed=self.onOpenFileClick)
        self.add(openFileButton)
        
        saveIcon = ImageIcon("../../../resources/images/save.png")
        saveFileButton = JButton("Save", saveIcon, 
                                 actionPerformed=self.onSaveFileClick)
        self.add(saveFileButton)
        
        closeIcon = ImageIcon("../../../resources/images/close.png")
        closeFileButton = JButton("Close", closeIcon, 
                                  actionPerformed=self.onCloseFileClick)
        self.add(closeFileButton)

        #AddSeparator might need addSeparator(Dimension(20,20)) to be visible
        self.addSeparator()

        undoIcon = ImageIcon("../../../resources/images/undo.png")
        undoButton = JButton("Undo", undoIcon, 
                             actionPerformed=self.onUndoClick)
        self.add(undoButton)
        
        redoIcon = ImageIcon("../../../resources/images/redo.png")
        redoButton = JButton("Redo", redoIcon, 
                             actionPerformed=self.onRedoClick)
        self.add(redoButton)
        
        #AddSeparator might need addSeparator(Dimension(20,20)) to be visible
        self.addSeparator()

        validateIcon = ImageIcon("../../../resources/images/validate.png")
        validateButton = JButton("Validate", validateIcon, 
                             actionPerformed=self.onValidateClick)
        self.add(validateButton)
        
        lemmatiseIcon = ImageIcon("../../../resources/images/lemmatise.png")
        lemmatiseButton = JButton("Lemmatise", lemmatiseIcon, 
                             actionPerformed=self.onLemmatiseClick)
        self.add(lemmatiseButton)
        
        #AddSeparator might need addSeparator(Dimension(20,20)) to be visible
        self.addSeparator()
        
        unicodeIcon = ImageIcon("../../../resources/images/unicode.png")
        unicodeButton = JButton("Unicode", unicodeIcon, 
                             actionPerformed=self.onUnicodeClick)
        self.add(unicodeButton)
        
        #AddSeparator might need addSeparator(Dimension(20,20)) to be visible
        self.addSeparator()
        
        consoleIcon = ImageIcon("../../../resources/images/console.png")
        consoleButton = JButton("Console", consoleIcon, 
                             actionPerformed=self.onConsoleClick)
        self.add(consoleButton)
        
        #AddSeparator might need addSeparator(Dimension(20,20)) to be visible
        self.addSeparator()
        
        modelIcon = ImageIcon("../../../resources/images/model.png")
        modelButton = JButton("Model", modelIcon, 
                             actionPerformed=self.onModelClick)
        self.add(modelButton)
        
        #AddSeparator might need addSeparator(Dimension(20,20)) to be visible
        self.addSeparator()

        quitIcon = ImageIcon("../../../resources/images/quit.png")
        quitButton = JButton("Quit", quitIcon, 
                             actionPerformed=self.onQuitClick)
        self.add(quitButton)
        
    def onNewFileClick(self, event):
        print "Prompt save current, clear text area"
        self.controller.newFile()
        
    def onOpenFileClick(self, event):
        print "Browse for new file to open and load it in text area."
        self.controller.openFile()
        
    def onSaveFileClick(self, event):
        print "Browse for place to save current file."
        self.controller.saveFile()
        
    def onCloseFileClick(self, event):
        print "Prompt save current, clear text area."
        self.controller.closeFile()
        
    def onUndoClick(self, event):
        print "Undo last action."
        self.controller.undo()
        
    def onRedoClick(self, event):
        print "Redo last undone action."
        self.controller.redo()
        
    def onValidateClick(self, event):
        print "Validate current ATF, display errors in console panel."
        self.controller.validate("text area content or path to file?")
        
    def onLemmatiseClick(self, event):
        print "Lemmatise current ATF, display errors in console panel."    
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
        print "Change atfAreaView to model mode." 
        self.controller.displayModelView()
        
    def onQuitClick(self, event):
        print "Prompt save current, exit Nammu."
        self.controller.quit()
        
        