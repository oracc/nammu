'''
Created on 15 Apr 2015

Initializes the toolbar view and sets its layout.

@author: raquel-ucl
'''
from javax.swing import JToolBar, ImageIcon, JButton

from ..controller.ToolbarController import ToolbarController

class ToolbarView(JToolBar):
    
    def __init__(self):
        print "I'm the toolbar view"
        #self.controller = ToolbarController
        
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
        lemmatiseButton = JButton("Validate", lemmatiseIcon, 
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
        
    def onOpenFileClick(self, event):
        print "Browse for new file to open and load it in text area."
        
    def onSaveFileClick(self, event):
        print "Browse for place to save current file."
        
    def onCloseFileClick(self, event):
        print "Prompt save current, clear text area."
        
    def onUndoClick(self, event):
        print "Undo last action."
        
    def onRedoClick(self, event):
        print "Redo last undone action."
        
    def onValidateClick(self, event):
        print "Validate current ATF, display errors in console panel."
        
    def onLemmatiseClick(self, event):
        print "Lemmatise current ATF, display errors in console panel."    
        
    def onUnicodeClick(self, event):
        print "Change to Unicode keyboard."   
        
    def onConsoleClick(self, event):
        print "Toggle console panel."  
        
    def onModelClick(self, event):
        print "Change atfAreaView to model mode." 
    
    def onQuitClick(self, event):
        print "Prompt save current, exit Nammu."
        
        
        