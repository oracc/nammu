'''
Copyright 2015 - 2018 University College London.

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

from java.awt import BorderLayout, GridLayout, Color, Dimension
from javax.swing import JScrollPane, JPanel, JFrame, JComboBox, JTabbedPane
from javax.swing import JLabel, BoxLayout, JButton


class ModelView(JFrame):
    '''
    Initializes the ATF model view and sets its layout.
    '''
    def __init__(self, controller):
        '''
        Creates a new window displaying a schematic view of an ATF file,
        following the guidelines and mockup agreed with project owners.
        '''

        # Give reference to controller to delegate action response
        self.controller = controller

        # Get list of projects, languages and protocols from config settings
        self.languages = self.controller.config['languages']
        self.protocols = self.controller.config['protocols']
        self.projects = self.controller.config['projects']

        # Make text area occupy all available space and resize with parent
        # window
        self.setLayout(BorderLayout())

        self.mainPanel = JTabbedPane()
        self.mainPanel.setTabLayoutPolicy(JTabbedPane.SCROLL_TAB_LAYOUT)
        self.add(self.mainPanel, BorderLayout.CENTER)

        # Set empty dictionary of tab panels
        self.objectTabs = {}

        # Will need scrolling controls
        scrollingArea = JScrollPane(self.mainPanel)

        # Add notice panel
        self.add(self.addNotice(), BorderLayout.NORTH)

        # Add to parent panel
        self.add(scrollingArea, BorderLayout.CENTER)

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
        combo.setEditable(True)
        combo.setPreferredSize(Dimension(500, 20))
        combo.setSize(combo.getPreferredSize())
        combo.setMinimumSize(combo.getPreferredSize())
        combo.setMaximumSize(combo.getPreferredSize())

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
        metadataPanel.setLayout(GridLayout(3, 2))

        projectLabel = JLabel("Project: ")
        projectValue = JLabel(project)

        languageLabel = JLabel("Language: ")
        languageValue = JLabel(language)
        # If language code is in the settings, then display name instead
        # of code
        for lang, code in self.languages.iteritems():
            if code == language:
                languageValue.setText(lang)

        # TODO Protocols not yet in parsed object
        protocolsLabel = JLabel("ATF Protocols: ")
        protocolsBox = JComboBox(self.protocols)

        metadataPanel.add(projectLabel)
        metadataPanel.add(projectValue)
        metadataPanel.add(languageLabel)
        metadataPanel.add(languageValue)
        metadataPanel.add(protocolsLabel)
        metadataPanel.add(protocolsBox)

        # Add metadataPanel to object tab in main panel
        self.objectTabs[objectID].add(metadataPanel)

    def addNotice(self):
        """
        Add a panel that notifies the user about the model view not being
        ready yet.
        """
        panel = JPanel()
        panel.setBackground(Color.yellow)
        label = JLabel("Please note Nammu's model view is under "
                       "construction.")
        panel.add(label)
        return panel
