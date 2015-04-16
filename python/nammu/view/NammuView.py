'''
Created on 15 Apr 2015

Main View class. 
Initializes the view components and sets components layout.

@author: raquel-ucl
'''

from java.awt import BorderLayout, Font
#from java.awt.event import  *   
from javax.swing import JFileChooser, JTextArea, JScrollPane, JPanel, JMenuBar, \
    JMenu, JFrame, JOptionPane, AbstractAction, BorderFactory, BoxLayout, Box
from java.io import FileWriter, IOException
from java.lang import System,Integer
from ..view.MenuView import MenuView
from ..view.AtfAreaView import AtfAreaView
from ..view.ToolbarView import ToolbarView
from ..view.ConsoleView import ConsoleView
from ..controller.MenuController import MenuController
from ..controller.ConsoleController import ConsoleController
from ..controller.AtfAreaController import AtfAreaController
from ..controller.ToolbarController import ToolbarController
from __builtin__ import None

class NammuView(JFrame):

    def __init__(self, controller):
        print "I'm the main window!"
        
        #Give reference to controller to delegate action response
        self.controller = controller
        
        #All window components apart from the menu will go in the JFrame's 
        #content pane 
        self.setLayout(BorderLayout())
        
        #TODO
        #Create splitPane with two empty panels for the ATF edition/console area
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
    #def bind(self):
    #    self.setContentPane(content)
        
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
        self.setTitle("~ Nammu v0.0.1 ~")
        self.pack()
        self.setLocationRelativeTo(None)

        #Display Nammu window
        self.visible = 1
        
 