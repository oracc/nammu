// Modified from https://stackoverflow.com/questions/11000220/strange-text-wrapping-with-styled-text-in-jtextpane-with-java-7/11001972#11001972

import javax.swing.*;
import javax.swing.event.*;
import javax.swing.text.*;
import java.awt.*;

public class MyParagraphView extends ParagraphView {

    public MyParagraphView(Element elem) {
        super(elem);
    }
public void removeUpdate(DocumentEvent e, Shape a, ViewFactory f) {
    super.removeUpdate(e, a, f);
    resetBreakSpots();
}
public void insertUpdate(DocumentEvent e, Shape a, ViewFactory f) {
    super.insertUpdate(e, a, f);
    resetBreakSpots();
}

private void resetBreakSpots() {
    for (int i=0; i<layoutPool.getViewCount(); i++) {
        View v=layoutPool.getView(i);
        if (v instanceof MyLabelView) {
            ((MyLabelView)v).resetBreakSpots();
        }
    }
}

}
