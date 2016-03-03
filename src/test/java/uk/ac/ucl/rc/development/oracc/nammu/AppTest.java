package uk.ac.ucl.rc.development.oracc.nammu;

import org.python.core.Py;
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
public class AppTest {

    public void testApp() throws PyException {
      PySystemState systemState = Py.getSystemState();
      systemState.path.append(new PyString("target/jython-plugins-tmp/build/pytest"));
      systemState.path.append(new PyString("target/jython-plugins-tmp/build/py"));
      PythonInterpreter interpreter = new PythonInterpreter();
      systemState.__setattr__("_jy_interpreter", Py.java2py(interpreter));
      String command = "try:\n "
                     + "  import pytest\n "
                     + "  pytest.main()\n"
                     + "except "
                     + "  SystemExit: pass";
      interpreter.exec(command);
    }
}
