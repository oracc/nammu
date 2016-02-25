'''
Created on 15 Apr 2015

Initializes the ATF (edit/model) view and sets its layout.

@author: raquel-ucl
'''

from java.awt import Font, BorderLayout, Dimension, Color
from javax.swing import JEditorPane, JScrollPane, JPanel, BorderFactory
from javax.swing.text import DefaultHighlighter, StyleContext
from pyoracc.atf.atflex import AtfLexer

class AtfAreaView(JPanel):

    def __init__(self, controller):
        '''
        Creates default empty text area in a panel.
        It will contain the ATF file content, and allow text edition.
        It should highlight reserved words and suggest autocompletion or
        possible typos, a la IDEs like Eclipse.
        It might need refactoring so that there is a parent panel with two
        modes or contexts, depending on user choice: text view or model view.
        '''
        # Give reference to controller to delegate action response
        self.controller = controller

        # Make text area occupy all available space and resize with parent
        # window
        self.setLayout(BorderLayout())

        # Create text edition area
        self.editArea = JEditorPane()
        self.editArea.border = BorderFactory.createEmptyBorder(4, 4, 4, 4)
        self.editArea.font = Font("Monaco", Font.PLAIN, 14)

        # Will need scrolling controls
        scrollingText = JScrollPane(self.editArea)
        scrollingText.setPreferredSize(Dimension(1, 500))

        # Add to parent panel
        self.add(scrollingText, BorderLayout.CENTER)
        self.painter = DefaultHighlighter.DefaultHighlightPainter(Color.YELLOW)

    def paint_word(self, word):
        doc = self.editArea.getDocument()
        text = doc.getText(0, doc.getLength())
        start = 0
        here = text.find(word, start)
        hiliter = self.editArea.getHighlighter()
        while here > -1:
            hiliter.addHighlight(here, here + len(word), self.painter)
            start = here + len(word)
            here = text.find(word, start)

    def reset_paint(self):
        hiliter = self.editArea.getHighlighter()
        hiliter.removeAllHighlights()

    def paint_index(self, word):
        doc = self.editArea.getDocument()
        text = doc.getText(0, doc.getLength())
        start = 0
        here = text.find(word, start)
        hiliter = self.editArea.getHighlighter()
        while here > -1:
            hiliter.addHighlight(here, here + len(word), self.painter)
            start = here + len(word)
            here = text.find(word, start)

    def syntax_highlight(self):
        lexer = AtfLexer().lexer
        text = self.editArea.text
        hiliter = self.editArea.getHighlighter()
        splittext = text.split('\n')
        lexer.input(text)
        for tok in lexer:
            if tok.type == 'LEM':
                linelenght = len(splittext[tok.lineno])
                hiliter.addHighlight(tok.lexpos, tok.lexpos + linelenght,
                                     self.painter)
