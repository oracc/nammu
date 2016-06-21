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

from java.awt import GridLayout
from javax.swing import JFrame


class NewAtfView(JFrame):
    '''
    Prompt user to choose some options to create a template for a new ATF
    file.
    '''
    def __init__(self, controller, projects, languages, protocols):
        self.controller = controller
        self.projects = projects
        self.languages = languages
        self.protocols = protocols
        
    def display(self):
        '''
        Displays window.
        '''
        self.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        self.setTitle("New ATF template")
        self.pack()
        self.setLocationRelativeTo(None)
        self.visible = 1
    
    def build(self):
        '''
        Puts all the window components together in the JFrame
        '''
        layout = GridLayout(4, 5)
        
    def add_and_row(self):
        '''
        Builds the &-line row.
        '''
        pass
    
    def add_projects_row(self):
        '''
        Builds the projects row.
        '''
        pass
    
    def add_language_row(self):
        '''
        Builds the language row.
        '''
        pass
    
    def add_protocols_row(self):
        '''
        Builds the protocols row.
        '''
        pass
