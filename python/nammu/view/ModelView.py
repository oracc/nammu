'''
Created on 17 Apr 2015

Initializes the ATF model view and sets its layout.
Might be merged with AtfAreaView in the future.

@author: raquel-ucl
'''

from java.awt import BorderLayout, GridLayout
from javax.swing import JScrollPane, JPanel, JFrame, JComboBox, JTabbedPane, \
                        JLabel, BoxLayout, JButton
from __builtin__ import None

class ModelView(JFrame):
    
    def __init__(self, controller):
        '''
        Creates a new window displaying a schematic view of an ATF file, 
        following the guidelines and mockup agreed with project owners.
        '''
        
        # Give reference to controller to delegate action response
        self.controller = controller
        
        # Make text area occupy all available space and resize with parent window
        self.setLayout(BorderLayout())
        
        self.mainPanel = JTabbedPane()
        self.mainPanel.setTabLayoutPolicy(JTabbedPane.SCROLL_TAB_LAYOUT);
        self.add(self.mainPanel, BorderLayout.CENTER)
        
        # Set empty dictionary of tab panels
        self.objectTabs = {}

        # Will need scrolling controls
        scrollingArea = JScrollPane(self.mainPanel)
        
        # Add to parent panel
        self.add(scrollingArea, BorderLayout.CENTER)
        
        # TODO: Where to get/store this information?
        self.languages = { "akk-x-stdbab": "Akkadian Standard Babylonian", \
                          "akk": "Akkadian", "sux": "", "a":"", \
                          "akk-x-oldbab":"Akkadian Old Babylonian", "qpc": "", \
                          "na": "", "nb": "", "x/n": "", \
                          "akk-x-neoass": "Akkadian Neo Assyrian"}
        
        
    def addObject(self, objectID):
        """
        Creates new empty JPanel that'll contain the model for one object in 
        the ATF file.
        """
        objectPanel = JPanel()
        objectPanel.setLayout(BoxLayout(objectPanel, BoxLayout.PAGE_AXIS))
        
        self.objectTabs[objectID] = objectPanel
  
        
    def display(self): 
        """
        Put together all elements in main panel and display.
        """
        # Add all object tabs to window
        for objectID, tabPanel in self.objectTabs.iteritems():
            self.mainPanel.add(objectID, tabPanel)
        
        # Set up main model window
        self.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        self.setTitle("ATF Model View")
        self.pack()
        self.setLocationRelativeTo(None)

        # Display model window
        self.visible = 1
        
        
    def addLine(self, objectID, category, text):
        """
        Add a new panel containing the text corresponding to one line in the 
        ATF file. 
        This panel will show the line type (ruling, comment, text, 
        translation...), followed by the line content and a group of icons to 
        add, edit or remove the line.
        """
        linePanel = JPanel()
        linePanel.setLayout(BorderLayout())
        
        label = JLabel(category)
        
        combo = JComboBox(text)
        
        buttonsPanel = JPanel()
        addButton = JButton("Add")
        editButton = JButton("Edit")
        deleteButton = JButton("Delete")
        buttonsPanel.add(addButton)
        buttonsPanel.add(editButton)
        buttonsPanel.add(deleteButton)
        
        linePanel.add(label, BorderLayout.WEST)
        linePanel.add(combo, BorderLayout.CENTER)
        linePanel.add(buttonsPanel, BorderLayout.EAST)
        
        # Add metadataPanel to object tab in main panel
        self.objectTabs[objectID].add(linePanel)
    
    
    # Protocols not yet in model parsed object
    # def addMetadata(self, project, language, protocols):
    def addMetadata(self, objectID, project, language):
        """
        Add a JTable at the top of the object tab containing the metadata of
        the object presented in that tab.
        """
        metadataPanel = JPanel()
        # TODO: Need to count protocols to set up Grid dimension
        metadataPanel.setLayout(GridLayout(3,2))
        
        projectLabel = JLabel("Project: ")
        projectValue = JLabel(project)
        
        # TODO Check language not found
        languageLabel = JLabel("Language: ")
        languageValue = JLabel(self.languages[language])
        
        # TODO Protocols not yet in parsed object
        protocolsLabel = JLabel("ATF Protocols: ")
        protocolsBox = JComboBox()
        # for protocol in protocols:
        #     protocolBox.add(protocol)
        
        metadataPanel.add(projectLabel)
        metadataPanel.add(projectValue)
        metadataPanel.add(languageLabel)
        metadataPanel.add(languageValue)
        metadataPanel.add(protocolsLabel)
        metadataPanel.add(protocolsBox)
        
        # Add metadataPanel to object tab in main panel
        self.objectTabs[objectID].add(metadataPanel)
        
    
    # TODO: def addSide(self, sideType, content):