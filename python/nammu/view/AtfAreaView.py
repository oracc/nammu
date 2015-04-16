'''
Created on 15 Apr 2015

Initializes the ATF (edit/model) view and sets its layout.

@author: raquel-ucl
'''

from java.awt import Font, BorderLayout 
from javax.swing import JTextArea, JScrollPane, JPanel, BorderFactory

class AtfAreaView(JPanel):
    
    def __init__(self):
        print "I'm the ATF area view"
        #self.controller = AtfAreaController
        
        self.editArea = JTextArea()
        self.editArea.border = BorderFactory.createEmptyBorder(2,2,2,2)
        self.editArea.font=Font("monospaced", Font.PLAIN, 14)
        scrollingText = JScrollPane(self.editArea)
        self.add(scrollingText, BorderLayout.CENTER)
    
        