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
        self.tokencolorlu['AMPERSAND'] = ('green', True)
        for i in AtfLexer.protocols:
            self.tokencolorlu[i] = ('magenta', False)
        for i in AtfLexer.protocol_keywords:
            self.tokencolorlu[i] = ('magenta', False)
        for i in AtfLexer.structures:
            self.tokencolorlu[i] = ('violet', False)
        for i in AtfLexer.long_argument_structures:
            self.tokencolorlu[i] = ('violet', False)
        self.tokencolorlu['DOLLAR'] = ('orange', False)
        for i in AtfLexer.dollar_keywords:
            self.tokencolorlu[i] = ('orange', False)
        self.tokencolorlu['REFERENCE'] = ('base01', False)
        self.tokencolorlu['COMMENT'] = ('base1', True)
        for i in AtfLexer.translation_keywords:
            self.tokencolorlu[i] = ('green', False)
        self.tokencolorlu['LINELABEL'] = ('yellow', False)
        self.tokencolorlu['LEM'] = ('red', False)
        self.tokencolorlu['SEMICOLON'] = ('red', False)
        self.tokencolorlu['HAT'] = ('cyan', False)

        self.tokencolorlu['NOTE'] = {}
        self.tokencolorlu['NOTE']['flagged'] = ('violet', False)
        self.tokencolorlu['NOTE']['para'] = ('magenta', False)

        self.tokencolorlu['PROJECT'] = {}
        self.tokencolorlu['PROJECT']['flagged'] = ('magenta', False)
        self.tokencolorlu['PROJECT']['transctrl'] = ('green', False)
        self.tokencolorlu['default'] = ('black', False)

    def syntax_highlight(self):
        lexer = AtfLexer(skipinvalid=True).lexer
        text = self.editArea.text
        splittext = text.split('\n')
        lexer.input(text)
        # Reset all styling
        defaultcolor = self.tokencolorlu['default'][0]
        self.styledoc.setCharacterAttributes(0, len(text),
                                             self.colors[defaultcolor],
                                             True)
        for tok in lexer:
            if tok.type in self.tokencolorlu:
                if type(self.tokencolorlu[tok.type]) is dict:
                    # the token should be styled differently depending
                    # on state
                    try:
                        state = lexer.current_state()
                        color = self.tokencolorlu[tok.type][state][0]
                        styleline = self.tokencolorlu[tok.type][state][1]
                    except KeyError:
                        color = self.tokencolorlu['default'][0]
                        styleline = self.tokencolorlu['default'][1]
                else:
                    color = self.tokencolorlu[tok.type][0]
                    styleline = self.tokencolorlu[tok.type][1]
                if styleline:
                    mylength = len(splittext[tok.lineno-1])
                else:
                    mylength = len(tok.value)
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
