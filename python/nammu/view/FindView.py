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


import logging
from javax.swing import SpringLayout, JDialog, JFrame
from java.awt import Dialog

class FindView(JDialog):
    '''
    Prompt user to choose some options to find and replace text in ATF area.
    '''
    def __init__(self, controller):
        self.logger = logging.getLogger("NammuController")
        self.modalityType = Dialog.ModalityType.APPLICATION_MODAL
        self.controller = controller
        self.pane = self.getContentPane()

    def display(self):
        '''
        Displays window.
        '''
        # self.build()
        self.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        self.setResizable(False)
        self.setTitle("Find/Replace")
        self.pack()
        self.setLocationRelativeTo(None)
        self.visible = 1
