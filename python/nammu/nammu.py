from java.awt import BorderLayout, Font
from java.awt.event import  *
from javax.swing import JFileChooser, JTextArea, JScrollPane, JPanel, JMenuBar, \
    JMenu, JFrame, JOptionPane, AbstractAction, BorderFactory
from java.io import FileWriter, IOException
from java.lang import System,Integer

class Nammu(JFrame):
    #... Components
   _editArea=None
   _fileChooser = JFileChooser()

   #============================================================== constructor
   def __init__(self):

     #... Create actions for menu items, buttons, ...
     self._openAction = OpenAction(self)
     self._saveAction = SaveAction(self)
     self._exitAction = ExitAction(self)

     #... Create scrollable text area.
     self._editArea = JTextArea(15, 80)
     self._editArea.border=BorderFactory.createEmptyBorder(2,2,2,2)
     self._editArea.font=Font("monospaced", Font.PLAIN, 14)
     scrollingText = JScrollPane(self._editArea)

     #-- Create a content pane, set layout, add component.
     content = JPanel()
     content.setLayout(BorderLayout())
     content.add(scrollingText, BorderLayout.CENTER);

     #... Create menubar
     menuBar = JMenuBar()
     fileMenu = menuBar.add(JMenu("File"))
     fileMenu.setMnemonic('F')
     fileMenu.add(self._openAction)       # Note use of actions, not text.
     fileMenu.add(self._saveAction)
     fileMenu.addSeparator()
     fileMenu.add(self._exitAction)

     #... Set window content and menu.
     self.setContentPane(content)
     self.setJMenuBar(menuBar)

     #... Set other window characteristics.
     self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
     self.setTitle("~ Nammu ~")
     self.pack()
     self.setLocationRelativeTo(None)
     self.visible=1

#//////////////////////////////////////////////// inner class OpenAction
class OpenAction(AbstractAction):
   #============================================= constructor
   def __init__(self,outer):  # outer instance.
     AbstractAction.__init__(self,"Open...")
     self.outer=outer
     self.putValue(AbstractAction.MNEMONIC_KEY, Integer(ord('O')))

   #========================================= actionPerformed
   def actionPerformed(self, e):
     retval = self.outer._fileChooser.showOpenDialog(self.outer)
     if retval==JFileChooser.APPROVE_OPTION:
       f = self.outer._fileChooser.getSelectedFile()
       try:
         reader = FileReader(f)
         self.outer._editArea.read(reader, "")  # Use TextComponent read
       except IOException,ioex:
         System.out.println(e);
         System.exit(1);

#////////////////////////////////////////////////// inner class SaveAction
class SaveAction(AbstractAction):
   #============================================= constructor
   def __init__(self,outer):
     AbstractAction.__init__(self,"Save...")
     self.outer=outer
     self.putValue(AbstractAction.MNEMONIC_KEY, Integer(ord('S')))

   #========================================= actionPerformed
   def actionPerformed(self, e):
     retval = self.outer._fileChooser.showSaveDialog(self.outer)
     if retval == JFileChooser.APPROVE_OPTION:
       f = self.outer._fileChooser.getSelectedFile()
       try:
         writer = FileWriter(f)
         self.outer._editArea.write(writer)  # TextComponent write
       except IOException,ioex:
         JOptionPane.showMessageDialog(self.outer, ioex)
         System.exit(1)

#/////////////////////////////////////////////////// inner class ExitAction
class ExitAction(AbstractAction):

   #============================================= constructor
   def __init__(self,outer):
     AbstractAction.__init__(self,"Exit")
     self.outer=outer
     self.putValue(AbstractAction.MNEMONIC_KEY, Integer(ord('X')))

   #========================================= actionPerformed
   def actionPerformed(self, e):
     System.exit(0);
     
     