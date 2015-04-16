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

    def __init__(self):
        print "I'm the main window!"
        
        #All window components apart from the menu will go in the JFrame's 
        #content pane 
        #self.getContentPane().setLayout(BorderLayout)
      

        
        #Assign view controller
        #self.controller = controller
        
        #Initialise Nammu components
        #menu = MenuView(MenuController)
        #atfArea = AtfAreaView(AtfAreaController)
        #toolbar = ToolbarView(ToolbarController)
        #console = ConsoleView(ConsoleController)
        
        
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
        
    
    #... Components
    #editArea = None
    #fileChooser = JFileChooser()

    #============================================================== constructor
#     def __init__(self):
#         
#         #... Create actions for menu items, buttons, ...
#         self.openAction = OpenAction(self)
#         self.saveAction = SaveAction(self)
#         self.exitAction = ExitAction(self)
# 
#         #... Create scrollable text area.
#         self.editArea = JTextArea(15, 80)
#         self.editArea.border=BorderFactory.createEmptyBorder(2,2,2,2)
#         self.editArea.font=Font("monospaced", Font.PLAIN, 14)
#         scrollingText = JScrollPane(self.editArea)
# 
#         #-- Create a content pane, set layout, add component.
#         content = JPanel()
#         content.setLayout(BorderLayout())
#         content.add(scrollingText, BorderLayout.CENTER);
# 
#         #... Create menubar
#         menuBar = JMenuBar()
#         fileMenu = menuBar.add(JMenu("File"))
#         fileMenu.setMnemonic('F')
#         fileMenu.add(self.openAction)       # Note use of actions, not text.
#         fileMenu.add(self.saveAction)
#         fileMenu.addSeparator()
#         fileMenu.add(self.exitAction)
#     
#         #... Set window content and menu.
#         self.setContentPane(content)
#         self.setJMenuBar(menuBar)
#     
#         #... Set other window characteristics.
#         self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
#         self.setTitle("~ Nammu ~")
#         self.pack()
#         self.setLocationRelativeTo(None)
#         self.visible=1
#         
#     def run(self):
#         print "Controller can run but it can't hide!"
# 
# #//////////////////////////////////////////////// inner class OpenAction
# class OpenAction(AbstractAction):
#    #============================================= constructor
#    def __init__(self,outer):  # outer instance.
#      AbstractAction.__init__(self,"Open...")
#      self.outer=outer
#      self.putValue(AbstractAction.MNEMONIC_KEY, Integer(ord('O')))
# 
#    #========================================= actionPerformed
#    def actionPerformed(self, e):
#      retval = self.outer.fileChooser.showOpenDialog(self.outer)
#      if retval==JFileChooser.APPROVE_OPTION:
#        f = self.outer.fileChooser.getSelectedFile()
#        try:
#          reader = FileReader(f)
#          self.outer.editArea.read(reader, "")  # Use TextComponent read
#        except IOException,ioex:
#          System.out.println(e);
#          System.exit(1);
# 
# #////////////////////////////////////////////////// inner class SaveAction
# class SaveAction(AbstractAction):
#    #============================================= constructor
#    def __init__(self,outer):
#      AbstractAction.__init__(self,"Save...")
#      self.outer=outer
#      self.putValue(AbstractAction.MNEMONIC_KEY, Integer(ord('S')))
# 
#    #========================================= actionPerformed
#    def actionPerformed(self, e):
#      retval = self.outer.fileChooser.showSaveDialog(self.outer)
#      if retval == JFileChooser.APPROVE_OPTION:
#        f = self.outer.fileChooser.getSelectedFile()
#        try:
#          writer = FileWriter(f)
#          self.outer.editArea.write(writer)  # TextComponent write
#        except IOException,ioex:
#          JOptionPane.showMessageDialog(self.outer, ioex)
#          System.exit(1)
# 
# #/////////////////////////////////////////////////// inner class ExitAction
# class ExitAction(AbstractAction):
# 
#    #============================================= constructor
#    def __init__(self,outer):
#      AbstractAction.__init__(self,"Exit")
#      self.outer=outer
#      self.putValue(AbstractAction.MNEMONIC_KEY, Integer(ord('X')))
# 
#    #========================================= actionPerformed
#    def actionPerformed(self, e):
#      System.exit(0);