'''
Copyright 2015 - 2018 University College London.

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

from java.awt import BorderLayout, Dimension, Point
from java.awt.event import KeyListener, AdjustmentListener
from java.awt.ComponentOrientation import RIGHT_TO_LEFT, LEFT_TO_RIGHT
from javax.swing import JScrollPane, JPanel, JSplitPane, UIManager
from javax.swing.text import StyleConstants
from javax.swing.undo import UndoManager, CompoundEdit
from javax.swing.event import UndoableEditListener, DocumentListener

from swingutils.threads.swing import runSwingLater

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

        # Short hand for edit area and line numbers area
        self.edit_area = self.controller.edit_area
        self.line_numbers_area = self.controller.line_numbers_area

        # Create secondary text area for split view
        self.secondary_area = self.controller.secondary_area
        self.secondary_line_numbers = self.controller.secondary_line_numbers

        # Create arabic translation text area for arabic edition
        self.arabic_area = self.controller.arabic_area
        self.arabic_line_numbers = self.controller.arabic_line_numbers

        # Set undo/redo manager to edit area
        self.undo_manager = UndoManager()
        self.undo_manager.limit = 3000
        self.edit_listener = AtfUndoableEditListener(self.undo_manager)
        self.edit_area.getDocument().addUndoableEditListener(
                                                        self.edit_listener)

        # Sort out layout by synch-ing line numbers and text area and putting
        # only the text area in a scroll pane as indicated in the
        # TextLineNumber tutorial.
        self.edit_area.setPreferredSize(Dimension(1, 500))
        self.container = JScrollPane(self.edit_area)
        self.container.setRowHeaderView(self.line_numbers_area)
        self.add(self.container, BorderLayout.CENTER)

        self.vert_scroll = self.container.getVerticalScrollBar()
        self.vert_scroll.addAdjustmentListener(atfAreaAdjustmentListener(self))

        # Key listener that triggers syntax highlighting, etc. upon key release
        self.edit_area.addKeyListener(AtfAreaKeyListener(self))
        # Also needed in secondary area:
        self.secondary_area.addKeyListener(AtfAreaKeyListener(self))
        # Also needed in arabic translation area:
        self.arabic_area.addKeyListener(AtfAreaKeyListener(self))
        self.arabic_area.setComponentOrientation(RIGHT_TO_LEFT)

        # Add a document listener to track changes to files
        docListener = atfAreaDocumentListener(self)
        self.edit_area.getDocument().addDocumentListener(docListener)

        # instance variable to store a record of the text contents prior to the
        # most recent change. Needed so that the different listeners can access
        # this to handle error line updating.
        self.oldtext = ''

    def toggle_split(self, split_orientation=None):
        '''
        Clear ATF edit area and repaint chosen layout (splitscreen/scrollpane).
        '''
        # Remove all existent components in parent JPanel
        self.removeAll()
        # Check what editor view to toggle
        self.setup_edit_area(split_orientation)
        # Revalitate is needed in order to repaint the components
        self.revalidate()
        self.repaint()
        self.controller.syntax_highlight()

    def toggle_split_arabic(self, split_orientation,
                            atf_body, atf_translation):
        '''
        Clear ATF edit area and repaint chosen layout (splitscreen/scrollpane).
        '''
        # Remove all existent components in parent JPanel
        self.removeAll()
        # Check what editor view to toggle
        self.setup_edit_area(split_orientation, arabic=True)
        # Separate body (in English) form translation (in Arabic) in different
        # panels.
        self.edit_area.setText(atf_body)
        self.arabic_area.setText(atf_translation)
        # Revalidate is needed in order to repaint the components
        self.revalidate()
        self.repaint()
        self.controller.syntax_highlight()

    def setup_edit_area(self, split_orientation=None, arabic=False):
        '''
        Check if the ATF text area is being displayed in a split editor.
        If so, resets to normal JScrollPane. If not, splits the screen.
        '''
        if isinstance(self.container, JSplitPane) and not arabic:
            # If Nammu is already displaying a split pane, reset to original
            # setup
            self.container = JScrollPane(self.edit_area)
            self.container.setRowHeaderView(self.line_numbers_area)
            self.container.setVisible(True)
            self.add(self.container, BorderLayout.CENTER)
            self.controller.controller.arabic_edition_on = False

            # Reset the scroll listener
            self.vert_scroll = self.container.getVerticalScrollBar()
            listener = atfAreaAdjustmentListener(self)
            self.vert_scroll.addAdjustmentListener(listener)
        else:
            # If there is not a split pane, create both panels and setup view
            main_editor = JScrollPane(self.edit_area)
            main_editor.setRowHeaderView(self.line_numbers_area)
            if arabic:
                secondary_editor = JScrollPane(self.arabic_area)
                secondary_editor.setRowHeaderView(self.arabic_line_numbers)
                self.controller.controller.arabic_edition_on = True
            else:
                secondary_editor = JScrollPane(self.secondary_area)
                secondary_editor.setRowHeaderView(self.secondary_line_numbers)
                self.controller.controller.arabic_edition_on = False
            self.container = JSplitPane(split_orientation,
                                        main_editor,
                                        secondary_editor)
            self.container.setDividerSize(5)
            self.container.setVisible(True)
            self.container.setDividerLocation(0.5)
            self.container.setResizeWeight(0.5)
            self.add(self.container, BorderLayout.CENTER)

            # Need to add scroll listeners to the scrollbars in the two panes
            topscroll = self.container.leftComponent.getVerticalScrollBar()
            bottomscroll = self.container.rightComponent.getVerticalScrollBar()
            topscroll.addAdjustmentListener(atfAreaAdjustmentListener(self))
            bottomscroll.addAdjustmentListener(atfAreaAdjustmentListener(self))

    def get_viewport_top_bottom(self, viewport):
        '''
        returns the top and bottom caret positions for a given viewport
        '''
        extent = viewport.getExtentSize()
        top_left_position = viewport.getViewPosition()
        top_left_char = self.edit_area.viewToModel(top_left_position)
        bottom_left_position = Point(top_left_position.x,
                                     top_left_position.y + extent.height)
        bottom_left_char = self.edit_area.viewToModel(bottom_left_position)

        # Something has gone wrong. Assume that top_left should be at the start
        # of the file
        if top_left_char >= bottom_left_char:
            top_left_char = 0

        # Get the text in the full edit area
        text = self.controller.edit_area.getText()

        # Pad the top of the viewport to capture up to the nearest header and
        # the bottom by 2 lines
        top_ch = self.controller.pad_top_viewport_caret(top_left_char, text)
        bottom_ch = self.controller.pad_bottom_viewport_caret(bottom_left_char,
                                                              text)

        return top_ch, bottom_ch

    def get_viewport_carets(self):
        '''
        Get the top left and bottom left caret position of the viewports on
        screen. If we have a split window, the carets will span both viewports
        and will give the range from the top of the file block to the lower
        extent of the two viewports.
        '''
        try:
            # Assumes a single edit pane
            viewport = self.container.getViewport()
            top_ch, bottom_ch = self.get_viewport_top_bottom(viewport)

        except:
            # Otherwise we have a split pane
            viewport_l = self.container.leftComponent.getViewport()
            viewport = self.container.rightComponent.getViewport()
            top_ch, bottom_ch = self.get_viewport_top_bottom(viewport)
            top_ch_l, bottom_ch_l = self.get_viewport_top_bottom(viewport_l)

            if bottom_ch_l > bottom_ch:
                bottom_ch = bottom_ch_l

        return top_ch, bottom_ch

    def refresh(self):
        '''
        Restyle edit area using user selected appearance settings.
        '''

        config = self.controller.controller.config

        # Create a new font with the new size
        font = set_font(config['edit_area_style']['fontsize']['user'])

        # Update the sytnax highlighter font params, so our changes are not
        # superceded
        self.controller.syntax_highlighter.font = font
        self.controller.syntax_highlighter.setup_attribs()

        attrs = self.controller.edit_area.getInputAttributes()
        StyleConstants.setFontSize(attrs, font.getSize())

        # Get the Styledoc so we can update it
        doc = self.controller.edit_area.getStyledDocument()

        # Apply the new fontsize to the whole document
        doc.setCharacterAttributes(0, doc.getLength() + 1, attrs, False)


class atfAreaDocumentListener(DocumentListener):
    def __init__(self, areaview):
        self.areaviewcontroller = areaview.controller
        self.areaview = areaview

    def errorUpdate(self, e, text, flag):
        '''
        Method to handle the updating of error lines.
        flag indicates whether the error lines need incremented ('insert')
        or decrmented ('remove').
        '''

        # Only need to do this if we have error_lines
        if self.areaviewcontroller.validation_errors == {}:
            return

        # Gets the position and length of the edit to the document
        length = e.getLength()
        offset = e.getOffset()

        # Slice out the edited text
        edited = text[offset:length + offset]

        if '\n' in edited:
            no_of_newlines = edited.count('\n')

            # Get the line no of the caret postion
            caret_line = self.areaviewcontroller.edit_area.get_line_num(offset)

            # Call our error line update method here, passing no_of_newlines
            self.areaviewcontroller.update_error_lines(caret_line,
                                                       no_of_newlines,
                                                       flag)

    def changedUpdate(self, e):
        '''
        Must be implemented to avoid NotImplemented errors
        '''
        pass

    def insertUpdate(self, e):
        '''
        Listen for an insertion to the document.
        '''
        text = self.areaviewcontroller.edit_area.getText()
        self.errorUpdate(e, text, 'insert')

    def removeUpdate(self, e):
        '''
        Listen for a removal from the document
        '''
        # Get the text prior to this edit event
        text = self.areaview.oldtext
        self.errorUpdate(e, text, 'remove')


class atfAreaAdjustmentListener(AdjustmentListener):
    def __init__(self, areaview):
        self.areaviewcontroller = areaview.controller
        self.areaview = areaview

    def adjustmentValueChanged(self, e):
        if not e.getValueIsAdjusting():
            runSwingLater(self.areaviewcontroller.controller.initHighlighting)


class AtfAreaKeyListener(KeyListener):
    """
    Listens for user releasing keys to reload the syntax highlighting and the
    line numbers (they'll need to be redrawn when a new line or block is added
    or removed).
    """
    def __init__(self, areaview):
        self.areaviewcontroller = areaview.controller
        self.areaview = areaview

    def keyReleased(self, ke):
        # Make sure we only syntax highlight when the key pressed is not an
        # action key (i.e. arrows, F1, ...) or is not shift, ctrl, alt, caps
        # lock or cmd.
        if ((not ke.isActionKey()) and
                (ke.getKeyCode() not in (16, 17, 18, 20, 157))):
            top_l_char, bottom_l_char = self.areaview.get_viewport_carets()
            self.areaviewcontroller.syntax_highlight(top_l_char, bottom_l_char)

    # We have to implement these since the baseclass versions
    # raise non implemented errors when called by the event.
    def keyPressed(self, ke):
        # Set the oldtext parameter, which stores the contents of the textfield
        # prior to the edits triggered by the keypress event. Needed for
        # tracking error highlighting on removal of lines.
        self.areaview.oldtext = self.areaviewcontroller.edit_area.getText()

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
        self.deletion = UIManager.getString('AbstractDocument.deletionText')
        self.addition = UIManager.getString('AbstractDocument.additionText')

    def force_start_compound(self):
        """
        Wraps list of interactions with the text area that'll cause several
        significant edit events that we want to put together in a compound
        edit.
        """
        empty_compound = CompoundEdit()
        if not self.must_compound:
            self.must_compound = True
            if not self.current_compound.equals(empty_compound):
                self.current_compound.end()
                self.undo_manager.addEdit(self.current_compound)
            self.current_compound = CompoundEdit()

    def force_stop_compound(self):
        self.current_compound.end()
        self.undo_manager.addEdit(self.current_compound)
        self.must_compound = False

    def undoableEditHappened(self, event):
        edit = event.getEdit()
        edit_type = edit.getPresentationName()

        # If significant INSERT/REMOVE event happen, end and add current
        # edit compound to undo_manager and start a new one.
        if ((edit_type == self.addition or edit_type == self.deletion) and
                not self.must_compound):
            # Explicitly end compound edits so their inProgress flag goes
            # to false. Note undo() only undoes compound edits when they
            # are not in progress.
            self.current_compound.end()
            self.current_compound = CompoundEdit()
            self.undo_manager.addEdit(self.current_compound)

        # Always add current edit to current compound
        self.current_compound.addEdit(edit)
