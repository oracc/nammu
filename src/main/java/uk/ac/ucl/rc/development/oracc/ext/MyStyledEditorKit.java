// Modified from https://stackoverflow.com/questions/11000220/strange-text-wrapping-with-styled-text-in-jtextpane-with-java-7/11001972#11001972

import javax.swing.*;
import javax.swing.event.*;
import javax.swing.text.*;

public class MyStyledEditorKit extends StyledEditorKit {
    private MyFactory factory;

    public ViewFactory getViewFactory() {
        if (factory == null) {
            factory = new MyFactory();
        }
        return factory;
    }

}
