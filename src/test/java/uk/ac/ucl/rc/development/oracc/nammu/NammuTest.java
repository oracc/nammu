/**
 * Copyright 2015 - 2017 University College London.
 * 
 * This file is part of Nammu.
 *
 * Nammu is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * Nammu is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with Nammu.  If not, see <http://www.gnu.org/licenses/>.
 * 
 */

package uk.ac.ucl.rc.development.oracc.nammu;

import org.junit.Test;
import static org.junit.Assert.assertEquals;
import org.python.core.Py;
import org.python.core.PyInteger;
import org.python.core.PyString;
import org.python.core.PyException;
import org.python.core.PySystemState;
import org.python.util.PythonInterpreter;
/**
 * This is the entry point for Nammu's tests.
 *
 * It sets up the Jython interpreter and ensures that it can find py.test.
 * It calls Py.test to run all the python tests in Nammu.
 *
 */
public class NammuTest {

    @Test
    public void testNammu() throws PyException {
      PySystemState systemState = Py.getSystemState();
      systemState.path.append(new PyString("target/jython-plugins-tmp/build/pytest"));
      systemState.path.append(new PyString("target/jython-plugins-tmp/build/py"));
      systemState.path.append(new PyString("target/jython-plugins-tmp/build/requests"));
      PythonInterpreter interpreter = new PythonInterpreter();
      systemState.__setattr__("_jy_interpreter", Py.java2py(interpreter));
      String command = "try:\n "
                     + "  import pytest\n "
                     + "  testresult = pytest.main(\" python/nammu/test/\")\n"
                     + "except "
                     + "  SystemExit: pass";
      interpreter.exec(command);
      PyInteger testresult = (PyInteger)interpreter.get("testresult");
      assertEquals(testresult.asInt(), 0);
    }
}
