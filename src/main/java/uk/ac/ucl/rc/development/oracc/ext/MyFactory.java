// Modified from https://stackoverflow.com/questions/11000220/strange-text-wrapping-with-styled-text-in-jtextpane-with-java-7/11001972#11001972

import javax.swing.*;
import javax.swing.event.*;
import javax.swing.text.*;
import java.awt.*;

public class MyFactory implements ViewFactory {
    public View create(Element elem) {
        String kind = elem.getName();
        if (kind != null) {
            if (kind.equals(AbstractDocument.ContentElementName)) {
                return new MyLabelView(elem);
            } else if (kind.equals(AbstractDocument.ParagraphElementName)) {
                return new MyParagraphView(elem);
            } else if (kind.equals(AbstractDocument.SectionElementName)) {
                return new BoxView(elem, View.Y_AXIS);
            } else if (kind.equals(StyleConstants.ComponentElementName)) {
                return new ComponentView(elem);
            } else if (kind.equals(StyleConstants.IconElementName)) {
                return new IconView(elem);
            }
        }

        // default to text display
        return new LabelView(elem);
    }
}
