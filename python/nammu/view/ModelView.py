'''
Created on 17 Apr 2015

Initializes the ATF model view and sets its layout.
Might be merged with AtfAreaView in the future.

@author: raquel-ucl
'''

from java.util import Vector
from java.awt import Font, BorderLayout, Dimension
from javax.swing import JTextArea, JScrollPane, JPanel, BorderFactory, JFrame, JComboBox, JTabbedPane
from __builtin__ import None

class ModelView(JFrame):
    
    def __init__(self, controller):
        '''
        Creates a new window displaying a schematic view of an ATF file, 
        following the guidelines and mockup agreed with project owners.
        '''
        
        #Give reference to controller to delegate action response
        self.controller = controller
        
        #Make text area occupy all available space and resize with parent window
        self.setLayout(BorderLayout())
        
        self.tabbedPanel = JTabbedPane()
        self.tabbedPanel.setTabLayoutPolicy(JTabbedPane.SCROLL_TAB_LAYOUT);
        self.add(self.tabbedPanel, BorderLayout.CENTER)

        
        #Will need scrolling controls
        scrollingArea = JScrollPane(self.tabbedPanel)
        scrollingArea.setPreferredSize(Dimension(600,400))
        
        #Add to parent panel
        self.add(scrollingArea, BorderLayout.CENTER)
        
        #Temp test
        metadataPanel = JPanel()
        metadataPanel.setLayout(BorderLayout())
        metadataField = JTextArea()
        metadataField.setText("#project: cams/gkab\n#atf: lang akk-x-stdbab\n#atf: use unicode\n#atf: use math")
        metadataPanel.add(metadataField, BorderLayout.NORTH)
        
        line1Content = Vector()
        line1Content.add(u"1.    [MU] 1.03-KAM {iti}AB GE\u2086 U\u2084 2-KAM")
        line1Content.add(u"#lem: \u0161atti[year]N; n; \u0162ebetu[1]MN; m\u016B\u0161a[at night]AV; \u016Bm[day]N; n")
        line1Content.add(u"1.    Year 63, \u0161ebetu (Month X), night of day 2:^1^")
        line1Content.add(u"^1^ A note to the translation.")
        
        line1Panel = JPanel()
        line1ComboBox = JComboBox(line1Content)
        line1Panel.add(line1ComboBox)
        
        panel1 = JPanel()
        panel1.setLayout(BorderLayout())
        panel1.add(metadataPanel, BorderLayout.NORTH)
        panel1.add(line1Panel, BorderLayout.CENTER)
        
        self.tabbedPanel.add("&X001001 = JCS 48, 089", panel1)
        
        
        
        
        
  
  
        
    def display(self):
        
        self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
        self.setTitle("ATF Model View")
        self.pack()
        self.setLocationRelativeTo(None)

        #Display Model window
        self.visible = 1
    
#     def addTab(self, title, panel):
#         tabbedPane.addTab( title, panel);
#         
#     def setProject(self):
#         
#     def setMetadata(self):
#         
#     def setObjectType(self, type):
#             
#     
#     def addReverse(self):
#         
#         
#     def addObverse(self):
        
        