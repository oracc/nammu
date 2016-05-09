'''
Created on 15 Apr 2015

Main View class.
Initializes the view components and sets components layout.

@author: raquel-ucl
'''

from java.awt import BorderLayout
from javax.swing import JFrame
from __builtin__ import None

class NammuView(JFrame):

    def __init__(self, controller):
        # Give reference to controller to delegate action response
        self.controller = controller

        # All window components apart from the menu will go in the JFrame's
        # content pane
        self.setLayout(BorderLayout())

        # TODO
        # Create splitPane with two empty panels for the ATF edition/console area
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


    def addAtfArea(self, atfAreaView):
        self.getContentPane().add(atfAreaView, BorderLayout.CENTER)


    def addConsole(self, consoleView):
        self.getContentPane().add(consoleView, BorderLayout.SOUTH)


    def display(self):
        self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
        self.setTitle("~ Nammu v0.0.4 - pre-release ~")
        self.pack()
        self.setLocationRelativeTo(None)

        # Display Nammu window
        self.visible = 1
