'''
Created on 15 Apr 2015

Main Controller class. 
Initialises the controller classes and displays the view.
Handles controller events.

@author: raquel-ucl
'''
from java.awt import BorderLayout, Font
#from java.awt.event import  *   
from javax.swing import JFileChooser, JTextArea, JScrollPane, JPanel, JMenuBar, \
    JMenu, JFrame, JOptionPane, AbstractAction, BorderFactory
from java.io import FileWriter, IOException
from java.lang import System,Integer
from ..view.NammuView import NammuView
from ..view.AtfAreaView import AtfAreaView
from ..view.ToolbarView import ToolbarView
from ..view.ConsoleView import ConsoleView
from ..view.MenuView import MenuView
from MenuController import MenuController
from ConsoleController import ConsoleController
from AtfAreaController import AtfAreaController
from ToolbarController import ToolbarController
from __builtin__ import None

class NammuController():
    
    def __init__(self):
        '''
        Initialise main controller of the application:
        1. For each component (menu, toolbar, ATF area, console)
            1.1. Create its view
            1.2. Create its controller referencing the corresponding view
        2. Create main view that'll bind all the components
        3. Create event/action handlers
        '''
        menuView = MenuView()
        menuController = MenuController(menuView)
        
        toolbarView = ToolbarView()
        toolbarController = ToolbarController(toolbarView)
        
        atfAreaView = AtfAreaView()
        atfAreaController = AtfAreaController(atfAreaView)
        
        consoleView = ConsoleView()
        consoleController = ConsoleController(consoleView)
    
        self.view = NammuView()
        self.view.addMenuBar(menuView)
        self.view.addToolBar(toolbarView)
#         self.view.add(atfAreaView)
#         self.view.add(consoleView)
   
        #Display view
        self.view.display()
        
        #Create actions - not sure I need any at these stage - maybe check ATF 
        #saved before closing? 
        #self.exitAction(self)
        
        
        
    
    
    