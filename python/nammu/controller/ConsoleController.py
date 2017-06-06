'''
Copyright 2015 - 2017 University College London.

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

from ..view.ConsoleView import ConsoleView
from javax.swing.text import StyleConstants, SimpleAttributeSet
from java.awt import Color


class ConsoleController(object):
    '''
    Creates the console view and handles console actions.
    '''
    def __init__(self, mainControler):
        # Create view with a reference to its controller to handle events
        self.view = ConsoleView(self)
        # Will also need delegating to parent presenter
        self.controller = mainControler
        # Need a record of previous messages so we can rebuild the html
        self.console_record = []

    def addText(self, text):
        # Wrap the new console message in p tags and add it to the record
        self.console_record.append('<p>{0}</p>'.format(text))

        # Update the console with all of the messages, we cant just insert
        # text as we have to insert within the <body> tags, so refreshing the
        # console with a new html page is the best solution
        self.view.edit_area.setText(''.join(self.console_record))
