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

# http://bugs.jython.org/issue2143
import site
from org.python.util import jython
jar_location = jython().getClass().getProtectionDomain().getCodeSource().getLocation().getPath()
import site
import os.path
site.addsitedir(os.path.join(jar_location, 'Lib/site-packages'))

from controller.NammuController import NammuController


def main():
    '''
    This is the Python entry point invoked from Java's entry point.
    '''
    NammuController()


if __name__ == '__main__':
    main()
