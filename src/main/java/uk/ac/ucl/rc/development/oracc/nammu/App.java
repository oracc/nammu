/**
 * This is the entry point for Nammu.
 * 
 * It sets up the Jython interpreter and ensures that it can find any requisite 
 * external libraries.
 * It call Python's entry point nammu.main.main()
 * 
 * @author raquel-ucl
 * 
 */

package uk.ac.ucl.rc.development.oracc.nammu;

import org.python.core.Py;
import org.python.core.PyException;
import org.python.core.PySystemState;
import org.python.util.PythonInterpreter;

public class App {
	
	 public static void main(String[] args) throws PyException {
	        PySystemState systemState = Py.getSystemState();
	        PythonInterpreter interpreter = new PythonInterpreter();
	        systemState.__setattr__("_jy_interpreter", Py.java2py(interpreter));
	        interpreter.exec("try:\n import nammu.main\n nammu.main.main()\nexcept SystemExit: pass");
	    }
}
