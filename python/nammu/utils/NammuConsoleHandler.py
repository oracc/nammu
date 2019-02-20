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

import logging
from logging import StreamHandler


class NammuConsoleHandler(StreamHandler):
    """
    Extends StreamHandler to make it print log messages in Nammu's console for
    the user to see.
    """
    def __init__(self, nammu_console):
        """
        Needs a reference to nammu to be able to get ahold of Nammu's console.
        """
        super(logging.StreamHandler, self).__init__()
        # Fixes an innocuous but ugly error message when exiting Nammu.
        self.stream = None
        self.nammu_console = nammu_console

    def emit(self, record):
        """
        This is the method that prints out the log message. Format the given
        record and send to Nammu's console for the user to see.
        """
        msg = self.format(record)
        self.nammu_console.addText(msg.decode('utf-8') + "\n")
