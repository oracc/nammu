'''
Created on 15 Apr 2015

Initializes the console view and sets its layout.

@author: raquel-ucl
'''

from java.awt import Font, BorderLayout, Color, Dimension
from javax.swing import JTextArea, JScrollPane, JPanel, BorderFactory

from ..controller.ConsoleController import ConsoleController

class ConsoleView(JPanel):
    
    def __init__(self):
        '''
        Creates default empty console-looking panel.
        It should be separated from the rest of the GUI so that users can choose
        to show or hide the console. Or should it be a split panel?
        This panel will display log and validation/lemmatization messages.
        It might need its own toolbar for searching, etc.
        It will also accept commands in later stages of development, if need be.
        '''
        
        #Give reference to controller to delegate action response
        #self.controller = ConsoleController
        
        #Make text area occupy all available space and resize with parent window
        self.setLayout(BorderLayout())
        
        #Create console-looking area
        self.editArea = JTextArea()
        self.editArea.border = BorderFactory.createEmptyBorder(4,4,4,4)
        self.editArea.font=Font("Courier New", Font.BOLD, 14)
        self.editArea.background = Color.BLACK
        self.editArea.foreground = Color.WHITE
        self.editArea.text = "Console started. Log will appear here."
        
        #Will need scrolling controls
        scrollingText = JScrollPane(self.editArea)
        scrollingText.setPreferredSize(Dimension(1,150))
        
        #Add to parent panel
        self.add(scrollingText, BorderLayout.CENTER)