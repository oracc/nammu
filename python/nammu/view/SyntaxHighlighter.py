'''
Copyright 2015 - 2017 University College London.

This file is part of Nammu.

Nammu is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Nammu is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Nammu.  If not, see <http://www.gnu.org/licenses/>.
'''
import re
from pyoracc.atf.atflex import AtfLexer
from java.awt import Color
from javax.swing.text import StyleContext, StyleConstants
from javax.swing.text import SimpleAttributeSet
from ..utils import set_font


class SyntaxHighlighter:
    def __init__(self, controller):
        self.controller = controller
        self.setup_syntax_highlight_colours()
        self.setup_syntax_highlight_tokens()
        self.font = set_font()
        self.setup_attribs()
        self.styledoc = controller.edit_area_styledoc
        self.lexer = AtfLexer(skipinvalid=True).lexer
        self.syntax_highlight_on = True

    def setup_attribs(self):
        '''
        Initialize colours, listeners and tokens to be syntax highlighted.
        '''
        def get_attribs(color, error=False, match=False):
            '''
            Closure to make the generation of font styling cleaner.
            Note closures need to be defined before being invoked.
            '''
            attribs = SimpleAttributeSet()
            StyleConstants.setFontFamily(attribs,
                                         self.font.getFamily())
            StyleConstants.setFontSize(attribs,
                                       self.font.getSize())
            StyleConstants.setForeground(attribs,
                                         Color(*self.colorlut[color]))
            # Add yellow background to error line styling
            # White if no error, otherwise it'll keep on being yellow forever
            if error:
                StyleConstants.setBackground(attribs, Color.yellow)
            elif match:
                # TODO: Change to another background colour Eleanor likes
                StyleConstants.setBackground(attribs, Color.yellow)
            else:
                StyleConstants.setBackground(attribs, Color.white)
            return attribs

        # Create two dictionaries of attributes, one per possible bg colour:
        # one with yellow background for errors and another with default bg.
        self.attribs = {}
        self.error_attribs = {}
        self.match_attribs = {}
        for color in self.colorlut:
            self.attribs[color] = get_attribs(color)
            self.error_attribs[color] = get_attribs(color, error=True)
            self.match_attribs[color] = get_attribs(color, match=True)

    def setup_syntax_highlight_colours(self):
        '''
        Initialises the colour lookup table for syntax highlighting.
        '''
        # Syntax highlighting colors based on SOLARIZED
        self.colorlut = {}

        # Black background tones
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

    def setup_syntax_highlight_tokens(self):
        '''
        Assings colours depending on type of token.
        '''
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
        self.tokencolorlu['OPENR'] = ('green', False)
        self.tokencolorlu['CLOSER'] = ('green', False)
        self.tokencolorlu['default'] = ('black', False)

    def syntax_highlight(self):
        '''
        Implements syntax highlighting based on pyoracc.
        If there are validation errors, highlight lines with errors.
        If user is doing find/replace, highlight matches.
        '''
        error_lines = self.controller.validation_errors.keys()
        if self.syntax_highlight_on:
            # Get text from styledoc
            area_length = self.styledoc.getLength()
            text = self.styledoc.getText(0, area_length)

            # Reset lexer and parse text
            self.lexer.input(text)
            self.lexer.lineno = 1
            while self.lexer.current_state() != 'INITIAL':
                self.lexer.pop_state()

            # Reset all styling
            defaultcolor = self.tokencolorlu['default'][0]

            # Break text into separate lines
            splittext = text.split('\n')

            # Keep background style from validation errors
            for line_num, line in enumerate(splittext, start=1):
                if str(line_num) in error_lines:
                    attribs = self.error_attribs[defaultcolor]
                else:
                    attribs = self.attribs[defaultcolor]
                atfCont = self.controller.controller.atfAreaController
                pos = atfCont.getPositionFromLine(text, line_num)
                self.styledoc.setCharacterAttributes(pos,
                                                     len(line) + 1,
                                                     attribs,
                                                     True)

        # Go through each token in the text, check which type it is to assign
        # a colour to it, check which position it is to set up default or
        # error background, etc.
        if self.syntax_highlight_on:
            for tok in self.lexer:
                if tok.type in self.tokencolorlu:
                    if type(self.tokencolorlu[tok.type]) is dict:
                        # the token should be styled differently depending
                        # on state
                        try:
                            state = self.lexer.current_state()
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
                    if str(tok.lineno) in error_lines:
                        attribs = self.error_attribs[color]
                    else:
                        attribs = self.attribs[color]
                    self.styledoc.setCharacterAttributes(tok.lexpos,
                                                         mylength,
                                                         attribs,
                                                         True)

    def syntax_highlight_off(self):
        '''
        Remove coloring.
        TODO: Make this properly!
        '''
        # Get text from styledoc
        area_length = self.styledoc.getLength()
        text = self.styledoc.getText(0, area_length)

        # Reset lexer and parse text
        self.lexer.input(text)
        self.lexer.lineno = 1
        while self.lexer.current_state() != 'INITIAL':
            self.lexer.pop_state()

        # Reset all styling
        defaultcolor = self.tokencolorlu['default'][0]

        # Break text into separate lines
        splittext = text.split('\n')

        # Keep background style from validation errors
        for line_num, line in enumerate(splittext, start=1):
            if str(line_num) in self.controller.validation_errors.keys():
                attribs = self.error_attribs[defaultcolor]
            else:
                attribs = self.attribs[defaultcolor]
            atfCont = self.controller.controller.atfAreaController
            pos = atfCont.getPositionFromLine(text, line_num)
            self.styledoc.setCharacterAttributes(pos[0],
                                                 len(line) + 1,
                                                 attribs,
                                                 True)

    def highlight_matches(self, matches, offset=0, current_match=None):
        '''
        Highlight text and apply highlight background for matches, taking
        the offset into account in case we are only searching on a selection.
        '''
        self.syntax_highlight()
        for match in matches:
            start = match.start() + offset
            length = match.end() - match.start()
            # Check if this match is the current match in the find next
            # iteration
            if match == current_match:
                self._highlight_match(start, length, Color.cyan)
            else:
                self._highlight_match(start, length, Color.lightGray)

    def _highlight_match(self, position, length, color):
        '''
        Changes attributes in text area to show highlighting.
        '''
        attribs = self.match_attribs['black']
        StyleConstants.setBackground(attribs, color)
        self.styledoc.setCharacterAttributes(position,
                                             length,
                                             attribs,
                                             True)
