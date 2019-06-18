'''
Copyright 2015 - 2019 University College London.

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

from java.awt import BorderLayout, Toolkit
from java.awt.event import KeyEvent, WindowAdapter
from javax.swing import JFrame, JSplitPane, KeyStroke, AbstractAction
from javax.swing import JComponent
import os


class NammuView(JFrame):
    '''
    Main View class.
    Initializes the view components and sets components layout.
    '''
    def __init__(self, controller):
        # Give reference to controller to delegate action response
        self.controller = controller

        # All window components apart from the menu will go in the JFrame's
        # content pane
        self.setLayout(BorderLayout())

        # Get key bindings configuration from settings
        key_strokes = self.controller.config['keystrokes']

        # Configure key bindings for undo/redo
        # First decide when key bindings can be triggered:
        condition = JComponent.WHEN_IN_FOCUSED_WINDOW

        # InputMap maps key strokes to actions in string format (e.g. 'undo')
        # ActionMap maps string actions (e.g. 'undo') with a custom
        # AbstractAction subclass.
        pane = self.getContentPane()
        for action, key in key_strokes.iteritems():
            key_stroke = KeyStroke.getKeyStroke(
                        getattr(KeyEvent, key),
                        Toolkit.getDefaultToolkit().getMenuShortcutKeyMask())
            pane.getInputMap(condition).put(key_stroke, action)
            pane.getActionMap().put(action, KeyStrokeAction(self, action))

        # Handle closing of the frame when clicking on the X button in title
        # bar.
        listener = CustomWindowListener(self)
        self.addWindowListener(listener)

        # TODO
        # Create splitPane with two empty panels for the ATF edition/console
        # area
#         splitPane = JSplitPane(JSplitPane.VERTICAL_SPLIT);
#
#         atfAreaPanel = JPanel()
#         consolePanel = JPanel()
#
#         splitPane.setTopComponent(atfAreaPanel)
#         splitPane.setBottomComponent(consolePanel)
#         splitPane.setDividerLocation(500);
#
#         self.add(splitPane)
#
    # def bind(self):
    #     self.setContentPane(content)

    def addMenuBar(self, menuView):
        self.setJMenuBar(menuView)

    def addToolBar(self, toolbarView):
        self.getContentPane().add(toolbarView, BorderLayout.NORTH)

    def addCenterPane(self, atfAreaView, consoleView):
        splitPane = JSplitPane(JSplitPane.VERTICAL_SPLIT)
        splitPane.setTopComponent(atfAreaView)
        splitPane.setBottomComponent(consoleView)
        splitPane.setDividerSize(5)
        self.getContentPane().add(splitPane, BorderLayout.CENTER)
        # Make console's high remain smaller compared to edit area
        splitPane.setResizeWeight(0.9)

    def set_title(self, unsaved=False):
        """
        Set the title bar to the base name of the currently open file.
        If `unsaved` is `True`, prepend "(*) " to the file name.
        """
        if self.controller.currentFilename is None:
            filename = "<New File>"
        else:
            filename = os.path.basename(self.controller.currentFilename)
        if unsaved:
            prefix = "(*) "
        else:
            prefix = ""
        self.setTitle("Nammu - {}{}".format(prefix, filename))

    def display(self):
        self.setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE)
        self.set_title()
        self.pack()
        self.setLocationRelativeTo(None)

        # Display Nammu window
        self.visible = 1


class KeyStrokeAction(AbstractAction):
    '''
    Needed to be assigned to key strokes via JComponent's ActionMap.
    '''
    def __init__(self, component, action):
        self.component = component
        self.action = action

    def actionPerformed(self, event):
        '''
        Overrides AbstractAction's actionPerform to executed the given action
        in the component's controller.
        '''
        getattr(self.component.controller, self.action)()


class CustomWindowListener(WindowAdapter):
    '''
    Handle closing of the JFrame.
    '''
    def __init__(self, frame):
        self.frame = frame

    def windowClosing(self, event):
        self.frame.controller.quit()
