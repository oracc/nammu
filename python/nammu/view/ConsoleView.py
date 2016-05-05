'''
Created on 15 Apr 2015

Initializes the console view and sets its layout.

@author: raquel-ucl
'''

from java.awt import Font, BorderLayout, Color, Dimension
from javax.swing import JTextArea, JScrollPane, JPanel, BorderFactory
from javax.swing.text import DefaultCaret

class ConsoleView(JPanel):

    def __init__(self, controller):
        '''
        Creates default empty console-looking panel.
        It should be separated from the rest of the GUI so that users can choose
        to show or hide the console. Or should it be a split panel?
        This panel will display log and validation/lemmatization messages.
        It might need its own toolbar for searching, etc.
        It will also accept commands in later stages of development, if need be.
        '''

        # Give reference to controller to delegate action response
        self.controller = controller

        # Make text area occupy all available space and resize with parent window
        self.setLayout(BorderLayout())

        #Create console-looking area
        self.editArea = JTextArea()
        self.editArea.border = BorderFactory.createEmptyBorder(4,4,4,4)
        self.editArea.font = Font("Courier New", Font.BOLD, 14)
        self.editArea.background = Color.BLACK
        self.editArea.foreground = Color.WHITE
        self.editArea.text = "Console started. Nammu's log will appear here.\n\n"

        # Disable writting in the console
        self.editArea.setEditable(False)

        # Will need scrolling controls
        scrollingText = JScrollPane(self.editArea)
        scrollingText.setPreferredSize(Dimension(1,150))

        # Make text area auto scroll down to last printed line
        caret = self.editArea.getCaret();
        caret.setUpdatePolicy(DefaultCaret.ALWAYS_UPDATE);

        # Add to parent panel
        self.add(scrollingText, BorderLayout.CENTER)


    def scroll(self):
        '''
        Scroll down to bottom.
        '''
        self.editArea.setCaretPosition(self.editArea.getDocument().getLength())
