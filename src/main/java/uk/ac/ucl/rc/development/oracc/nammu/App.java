package uk.ac.ucl.rc.development.oracc.nammu;

import org.python.core.Py;
import org.python.core.PyException;
import org.python.core.PySystemState;
import org.python.util.PythonInterpreter;

/**
 * This is the entry point for Nammu.
 *
 * It sets up the Jython interpreter and ensures that it can find any requisite
 * external libraries.
 * It calls Python's entry point nammu.main.main()
 *
 */
public class App {

    public static void main(final String[] args) throws PyException {
        PySystemState systemState = Py.getSystemState();
        PythonInterpreter interpreter = new PythonInterpreter();
        systemState.__setattr__("_jy_interpreter", Py.java2py(interpreter));
        String command = "try:\n "
                       + "  import nammu.main\n "
                       + "  nammu.main.main()\n"
                       + "except "
                       + "  SystemExit: pass";
        interpreter.exec(command);
    }
}
