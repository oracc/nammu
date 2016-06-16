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

from java.awt import BorderLayout
from javax.swing import JFrame, JSplitPane
from __builtin__ import None


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

    def display(self):
        self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
        self.setTitle("Nammu")
        self.pack()
        self.setLocationRelativeTo(None)

        # Display Nammu window
        self.visible = 1
