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
from java.awt import BorderLayout, Dimension, Color
from java.awt.event import KeyListener
from javax.swing import JScrollPane, JPanel, JSplitPane
from javax.swing.text import StyleContext, StyleConstants
from javax.swing.text import SimpleAttributeSet
from javax.swing.undo import UndoManager, CompoundEdit
from javax.swing.event import UndoableEditListener
from contextlib import contextmanager
from .AtfEditArea import AtfEditArea


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

        # Key listener that triggers syntax highlighting, etc. upon key release
        self.edit_area.addKeyListener(AtfAreaKeyListener(self.controller))
        # Also needed in secondary area:
        self.secondary_area.addKeyListener(AtfAreaKeyListener(self.controller))

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

    def setup_edit_area(self, split_orientation=None):
        '''
        Check if the ATF text area is being displayed in a split editor.
        If so, resets to normal JScrollPane. If not, splits the screen.
        '''
        if isinstance(self.container, JSplitPane):
            # If Nammu is already displaying a split pane, reset to original
            # setup
            self.container = JScrollPane(self.edit_area)
            self.container.setRowHeaderView(self.line_numbers_area)
            self.container.setVisible(True)
            self.add(self.container, BorderLayout.CENTER)
        else:
            # If there is not a split pane, create both panels and setup view
            main_editor = JScrollPane(self.edit_area)
            main_editor.setRowHeaderView(self.line_numbers_area)
            secondary_editor = JScrollPane(self.secondary_area)
            secondary_editor.setRowHeaderView(self.secondary_line_numbers)
            self.container = JSplitPane(split_orientation,
                                        main_editor,
                                        secondary_editor)
            self.container.setDividerSize(5)
            self.container.setVisible(True)
            self.container.setDividerLocation(0.5)
            self.container.setResizeWeight(0.5)
            self.add(self.container, BorderLayout.CENTER)


class AtfAreaKeyListener(KeyListener):
    """
    Listens for user releasing keys to reload the syntax highlighting and the
    line numbers (they'll need to be redrawn when a new line or block is added
    or removed).
    """
    def __init__(self, controller):
        self.controller = controller

    def keyReleased(self, ke):
        # Make sure we only syntax highlight when the key pressed is not an
        # action key (i.e. arrows, F1, ...) or is not shift, ctrl, alt, caps
        # lock or cmd.
        if ((not ke.isActionKey()) and
                (ke.getKeyCode() not in (16, 17, 18, 20, 157))):
            self.controller.syntax_highlight()

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
