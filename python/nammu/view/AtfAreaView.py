'''
Created on 15 Apr 2015

Initializes the ATF (edit/model) view and sets its layout.

@author: raquel-ucl
'''

from java.awt import Font, BorderLayout, Dimension
from javax.swing import JTextArea, JScrollPane, JPanel, BorderFactory

class AtfAreaView(JPanel):
    
    def __init__(self, controller):
        '''
        Creates default empty text area in a panel.
        It will contain the ATF file content, and allow text edition.
        It should highlight reserved words and suggest autocompletion or 
        possible typos, a la IDEs like Eclipse.
        It might need refactoring so that there is a parent panel with two modes
        or contexts, depending on user choice: text view or model view.
        '''
        #Give reference to controller to delegate action response
        self.controller = controller
        
        #Make text area occupy all available space and resize with parent window
        self.setLayout(BorderLayout())
        
        #Create text edition area
        self.editArea = JTextArea()
        self.editArea.border = BorderFactory.createEmptyBorder(4,4,4,4)
        self.editArea.font=Font("Monaco", Font.PLAIN, 14)
        
        #Will need scrolling controls
        scrollingText = JScrollPane(self.editArea)
        scrollingText.setPreferredSize(Dimension(1,500))
        
        #Add to parent panel
        self.add(scrollingText, BorderLayout.CENTER)
    
        