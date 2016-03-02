'''
Created on 15 Apr 2015

Initializes the ATF (edit/model) view and sets its layout.

@author: raquel-ucl
'''

from java.awt import Font, BorderLayout, Dimension, Color
from java.awt.event import KeyListener
from javax.swing import JTextPane, JScrollPane, JPanel, BorderFactory
from javax.swing.text import DefaultHighlighter, StyleContext, StyleConstants
from javax.swing.text import SimpleAttributeSet
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
        self.editArea = JTextPane()
        self.editArea.border = BorderFactory.createEmptyBorder(4, 4, 4, 4)
        self.editArea.font = Font("Monaco", Font.PLAIN, 14)
        self.styledoc = self.editArea.getStyledDocument()
        # Will need scrolling controls
        scrollingText = JScrollPane(self.editArea)
        scrollingText.setPreferredSize(Dimension(1, 500))

        # Add to parent panel
        self.add(scrollingText, BorderLayout.CENTER)

        sc = StyleContext.getDefaultStyleContext()
        # Syntax highlighting colors based on SOLARIZED
        self.colorlut = {}
        # Black backgroud tones
        self.colorlut['base03'] = (0, 43, 54)
        self.colorlut['base02'] = (7, 54, 66)
        # Content tones
        self.colorlut['base01'] = (88, 110, 117)
        self.colorlut['base00'] = (101, 123, 131)
        self.colorlut['base0'] = (131, 148, 150)
        self.colorlut['base1'] = (147, 161, 161)
        # White background tones
        self.colorlut['base2'] = (238, 232, 213)
        self.colorlut['base3'] = (253, 246, 227)
        # Accent Colors
        self.colorlut['yellow'] = (181, 137, 0)
        self.colorlut['orange'] = (203, 75, 22)
        self.colorlut['red'] = (220,  50, 47)
        self.colorlut['magenta'] = (211,  54, 130)
        self.colorlut['violet'] = (108, 113, 196)
        self.colorlut['blue'] = (38, 139, 210)
        self.colorlut['cyan'] = (42, 161, 152)
        self.colorlut['green'] = (133, 153, 0)
        self.colorlut['black'] = (0, 0, 0)

        self.colors = {}
        for color in self.colorlut:
            self.colors[color] = sc.addAttribute(
                                           SimpleAttributeSet.EMPTY,
                                           StyleConstants.Foreground,
                                           Color(*self.colorlut[color]))
        self.editArea.addKeyListener(AtfAreaKeyListener(self))

        self.tokencolorlu = {}
        self.tokencolorlu['AMPERSAND'] = ('green', True, 0)
        for i in AtfLexer.protocols:
            self.tokencolorlu[i] = ('magenta', False, 1)
        for i in AtfLexer.protocol_keywords:
            self.tokencolorlu[i] = ('magenta', False, 0)
        for i in set(AtfLexer.structures)-set(['NOTE']):
            self.tokencolorlu[i] = ('violet', False, 1)
        for i in AtfLexer.long_argument_structures:
            self.tokencolorlu[i] = ('violet', False, 1)
        self.tokencolorlu['DOLLAR'] = ('orange', False, 0)
        for i in AtfLexer.dollar_keywords:
            self.tokencolorlu[i] = ('orange', False, 0)
        self.tokencolorlu['REFERENCE'] = ('base01', False, 0)
        self.tokencolorlu['COMMENT'] = ('base1', True, 0)
        for i in AtfLexer.translation_keywords:
            self.tokencolorlu[i] = ('green', False, 0)
        self.tokencolorlu['LINELABEL'] = ('yellow', False, 0)
        self.tokencolorlu['LEM'] = ('red', False, 1)
        self.tokencolorlu['SEMICOLON'] = ('red', False, 0)
        self.tokencolorlu['HAT'] = ('cyan', False, 0)

    def syntax_highlight(self):
        lexer = AtfLexer(skipinvalid=True).lexer
        text = self.editArea.text
        splittext = text.split('\n')
        lexer.input(text)
        self.styledoc.setCharacterAttributes(0, len(text),
                                             self.colors['black'],
                                             True)
        for tok in lexer:
            if tok.type in self.tokencolorlu:
                color = self.tokencolorlu[tok.type][0]
                styleline = self.tokencolorlu[tok.type][1]
                offset = self.tokencolorlu[tok.type][2]
                if styleline:
                    mylength = len(splittext[tok.lineno-1])
                else:
                    mylength = len(tok.value) + offset
                self.styledoc.setCharacterAttributes(tok.lexpos, mylength,
                                                     self.colors[color],
                                                     True)


class AtfAreaKeyListener(KeyListener):
    def __init__(self, atfareaview):
        self.atfareaview = atfareaview

    def keyReleased(self, ke):
        self.atfareaview.syntax_highlight()

    # We have to implement these since the baseclass versions
    # raise non implemented errors when called by the event.
    def keyPressed(self, ke):
        pass

    def keyTyped(self, ke):
        # It would be more natural to use this event. However
        # this gives the string before typing
        pass
