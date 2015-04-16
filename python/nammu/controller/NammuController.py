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
            1.1 Create its controller, which will
                Create its own view referencing the corresponding controller
        2. Create main view that'll bind all the components
        3. Create event/action handlers - EventBus?
        '''
        
        menuController = MenuController(self)
        toolbarController = ToolbarController(self)
        atfAreaController = AtfAreaController(self)
        consoleController = ConsoleController(self)
    
        self.view = NammuView(self)
        self.view.addMenuBar(menuController.view)
        self.view.addToolBar(toolbarController.view)
        self.view.addAtfArea(atfAreaController.view)
        self.view.addConsole(consoleController.view)
   
        #Display view
        self.view.display()
        
        #Handle actions - eventBus?
        
        
        
    
    
    