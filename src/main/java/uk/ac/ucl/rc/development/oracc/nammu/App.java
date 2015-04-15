package uk.ac.ucl.rc.development.oracc.nammu;

import java.util.Properties;

import org.python.core.Py;
import org.python.core.PyException;
import org.python.core.PyString;
import org.python.core.PySystemState;
import org.python.util.PythonInterpreter;

public class App {
	
	 public static void main(String[] args) throws PyException {
	        PySystemState.initialize(
	            PySystemState.getBaseProperties(), 
	            new Properties(), args);

	        PythonInterpreter interpreter = new PythonInterpreter();
	        
	        PySystemState systemState = Py.getSystemState();

	        //Link some external python libraries installed via maven plugin 
	        systemState.path.append(new PyString("target/classes/Lib"));
	        
	        systemState.__setattr__("_jy_interpreter", Py.java2py(interpreter));
	        interpreter.exec("try:\n import nammu.main\n nammu.main.main()\nexcept SystemExit: pass");
	    }
}
