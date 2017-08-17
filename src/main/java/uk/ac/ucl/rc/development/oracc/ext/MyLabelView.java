// Modified from https://stackoverflow.com/questions/11000220/strange-text-wrapping-with-styled-text-in-jtextpane-with-java-7/11001972#11001972

import javax.swing.*;
import javax.swing.event.*;
import javax.swing.text.*;
import java.awt.*;


public class MyLabelView extends LabelView {

    boolean isResetBreakSpots=false;

    public MyLabelView(Element elem) {
        super(elem);
    }
    public View breakView(int axis, int p0, float pos, float len) {
        if (axis == View.X_AXIS) {
            resetBreakSpots();
        }
        return super.breakView(axis, p0, pos, len);
    }

    public void resetBreakSpots() {
        isResetBreakSpots=true;
        removeUpdate(null, null, null);
        isResetBreakSpots=false;
   }

    public void removeUpdate(DocumentEvent e, Shape a, ViewFactory f) {
        super.removeUpdate(e, a, f);
    }

    public void preferenceChanged(View child, boolean width, boolean height) {
        if (!isResetBreakSpots) {
            super.preferenceChanged(child, width, height);
        }
    }
}
