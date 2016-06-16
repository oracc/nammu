'''
Copyright 2015, 2016 University College London.

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
from java.awt import BorderLayout, Dimension, Color
from java.awt.event import KeyListener
from javax.swing import JScrollPane, JPanel
from javax.swing.text import StyleContext, StyleConstants
from javax.swing.text import SimpleAttributeSet
from javax.swing.undo import UndoManager, CompoundEdit
from javax.swing.event import UndoableEditListener
from contextlib import contextmanager
from pyoracc.atf.atflex import AtfLexer
from .AtfEditArea import AtfEditArea
from .LineNumbersArea import LineNumbersArea
from ..utils import set_font


class AtfAreaView(JPanel):
    '''
    Initializes the ATF (edit/model) view and sets its layout.
    '''
    def __init__(self, controller):
        '''
        Creates default empty text area in a panel for ATF edition.
        It has syntax highlighting based on the ATF parser (pyoracc).
        It also highlights line numbers where there are validations errors
        returned by the ORACC server.
        '''
        # Give reference to controller to delegate action response
        self.controller = controller

        # Make text area occupy all available space and resize with parent
        # window
        self.setLayout(BorderLayout())

        # Set font
        self.font = set_font()

        # Create text edition area
        self.editArea = AtfEditArea(self)

        # Create text panel to display the line numbers
        self.line_numbers_area = LineNumbersArea()

        # Needed by syntax highlighter
        self.edit_area_styledoc = self.editArea.getStyledDocument()
        self.line_numbers_styledoc = self.line_numbers_area.getStyledDocument()

        # Set undo/redo manager to edit area
        self.undo_manager = UndoManager()
        self.undo_manager.limit = 3000
        self.edit_listener = AtfUndoableEditListener(self.undo_manager)
        self.editArea.getDocument().addUndoableEditListener(self.edit_listener)

        # Create panel that'll contain the ScrollPane and the line numbers
        container = JPanel(BorderLayout())
        container.add(self.editArea, BorderLayout.CENTER)
        container.add(self.line_numbers_area, BorderLayout.WEST)

        # Will need scrolling controls that scroll line numbers and text lines
        # simultaneously
        scrollingText = JScrollPane(container)
        scrollingText.setPreferredSize(Dimension(1, 500))
        scrollingText.getVerticalScrollBar().setUnitIncrement(16)

        # Add to parent panel
        self.add(scrollingText, BorderLayout.CENTER)

        # Syntax highlight setup
        self.set_up_syntax_highlight()
        
        # Needs to be accessible from the AtfEditArea
        self.validation_errors = None
        
    def set_up_syntax_highlight(self):
        '''
        Initialize colours, listeners and tokens to be syntax highlighted.
        '''
        self.setup_syntax_highlight_colours()
    
        def get_attribs(color):
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
            return attribs
        
        # Create a dictionary of attributes, two per possible font colour:
        # one with yellow background for errors and another with default bg.
        self.attribs = {}
        for color in self.colorlut:
            self.attribs[color] = get_attribs(color)
        self.editArea.addKeyListener(AtfAreaKeyListener(self))
        self.setup_syntax_highlight_tokens()

    def error_highlight(self, validation_errors):
        """
        Highlights line numbers and text lines that have errors.
        Receives a dictionary with line numbers and error messages and repaints
        the line numbers and text lines to highlight errors.
        """
        if validation_errors:
            self.validation_errors = validation_errors
            for line_num, error in validation_errors.items():
                attribs = SimpleAttributeSet()
                StyleConstants.setFontFamily(attribs, self.font.getFamily())
                StyleConstants.setFontSize(attribs, self.font.getSize())
                StyleConstants.setForeground(attribs, Color.red)
                line_numbers_sd = self.line_numbers_area.getStyledDocument()
                edit_area_sd = self.editArea.getStyledDocument()
                text = self.line_numbers_area.text

                # Search for start position and length of line number
                if line_num in text:
                    match = re.search(line_num, text)
                    # This will return the position of the first substring
                    # matching the line num, so we won't run into problems like
                    # getting 122 when we are searching for 12 or 22.
                    position = match.start()
                    # Line numbers are as long as the number + 1 because it is
                    # followed by a colon
                    length = len(line_num) + 1
                    # Change style in line number panel
                    line_numbers_sd.setCharacterAttributes(position,
                                                           length,
                                                           attribs,
                                                           True)

                    # Calculate postion of text line
                    text = re.finditer(r"\n", self.editArea.text)
                    line_num = int(line_num)
                    if line_num >= 2:
                        pos = [m.start() for m in text][line_num - 2:line_num]
                    elif '\n' in self.editArea.text:
                        # If error is in first line, highlight it
                        pos = [0, self.editArea.text.index('\n')]
                    else:
                        # If no end of line, text is a one liner
                        pos = [0, len(self.editArea.text)]
                    length = pos[1] - pos[0]
                    # Highlight text line
                    attribs = SimpleAttributeSet()
                    StyleConstants.setFontFamily(attribs,
                                                 self.font.getFamily())
                    StyleConstants.setFontSize(attribs, self.font.getSize())
                    StyleConstants.setBackground(attribs, Color.yellow)
                    edit_area_sd.setCharacterAttributes(pos[0],
                                                        length,
                                                        attribs,
                                                        True)

    def syntax_highlight(self):
        """
        Implements syntax highlighting based on pyoracc.
        """
        lexer = AtfLexer(skipinvalid=True).lexer
        edit_area_length = self.edit_area_styledoc.getLength()
        text = self.edit_area_styledoc.getText(0,
                                               edit_area_length)
        splittext = text.split('\n')
        lexer.input(text)
        # Reset all styling
        defaultcolor = self.tokencolorlu['default'][0]
        attribs = self.attribs[defaultcolor]
        self.edit_area_styledoc.setCharacterAttributes(0,
                                                       len(text),
                                                       attribs,
                                                       True)
        for tok in lexer:
            if tok.type in self.tokencolorlu:
                if type(self.tokencolorlu[tok.type]) is dict:
                    # the token should be styled differently depending
                    # on state
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
                attribs = self.attribs[color]
                self.edit_area_styledoc.setCharacterAttributes(tok.lexpos,
                                                               mylength,
                                                               attribs,
                                                               True)

    def setup_syntax_highlight_colours(self):
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

    def repaint_line_numbers(self, n_lines):
        """
        Draws line numbers in corresponding panel.
        """
        # Create line numbers
        numbers = ""
        for line in range(n_lines + 1):
            numbers += str(line + 1) + ": \n"

        # Print in line numbers' area
        self.line_numbers_area.setText(numbers)


class AtfAreaKeyListener(KeyListener):
    """
    Listens for user releasing keys to reload the syntax highlighting and the
    line numbers (they'll need to be redrawn when a new line or block is added
    or removed).
    """
    def __init__(self, atfareaview):
        self.atfareaview = atfareaview

    def keyReleased(self, ke):
        self.atfareaview.syntax_highlight()
        # Check length hasn't changed, otherwise repaint line numbers
        number_lines = self.atfareaview.line_numbers_area.text.count('\n')
        text_lines = self.atfareaview.editArea.text.count('\n')
        if number_lines - 1 != text_lines:
            self.atfareaview.repaint_line_numbers(text_lines)

    # We have to implement these since the baseclass versions
    # raise non implemented errors when called by the event.
    def keyPressed(self, ke):
        pass

    def keyTyped(self, ke):
        # It would be more natural to use this event. However
        # this gives the string before typing
        pass


class AtfUndoableEditListener(UndoableEditListener):
    '''
    Overrides the undoableEditHappened functionality to group INSERT/REMOVE
    edit events with their associated CHANGE events (these correspond to
    highlighting only at the moment).
    TODO: Make compounds save whole words so undoing is not so much of a pain
          for the user.
    '''
    def __init__(self, undo_manager):
        self.undo_manager = undo_manager
        self.current_compound = CompoundEdit()
        self.must_compound = False

    @contextmanager
    def force_compound(self):
        """
        Wraps list of interactions with the text area that'll cause several
        significant edit events that we want to put together in a compound
        edit.
        """
        self.must_compound = False
        self.current_compound.end()
        self.undo_manager.addEdit(self.current_compound)
        try:
            yield
        finally:
            self.must_compound = False
            self.current_compound.end()
            self.undo_manager.addEdit(self.current_compound)

    def undoableEditHappened(self, event):
        edit = event.getEdit()
        edit_type = str(edit.getType())

        # If significant INSERT/REMOVE event happen, end and add current
        # edit compound to undo_manager and start a new one.
        if ((edit_type == "INSERT" or edit_type == "REMOVE") and
                not self.must_compound):
            # Explicitly end compound edits so their inProgress flag goes
            # to false. Note undo() only undoes compound edits when they
            # are not in progress.
            self.current_compound.end()
            self.current_compound = CompoundEdit()
            self.undo_manager.addEdit(self.current_compound)

        # Always add current edit to current compound
        self.current_compound.addEdit(edit)
