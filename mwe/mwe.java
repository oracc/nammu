import javax.swing.*;
import javax.swing.text.JTextComponent;
import javax.swing.text.Document;
import javax.swing.text.SimpleAttributeSet;
import javax.swing.text.StyleConstants;
import java.text.Bidi;
import java.awt.*;


public class mwe {
    public static void main(String[] args)throws Exception {
        UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                createAndShowGUI();
            }
        });
    }

    final static String sampleTextTop = "This is a line of english.\n\n@translation parallel ar project\n\n";
    final static String sampleTextBottom = "\u200F هذا هو الاختبا";

    private static void createAndShowGUI() {
        final JFrame frame = new JFrame("test");
        final JTextPane textpane=new JTextPane();
        Document doc = textpane.getDocument();

        SimpleAttributeSet attribs_right = new SimpleAttributeSet();
        StyleConstants.setAlignment(attribs_right, StyleConstants.ALIGN_RIGHT);

        SimpleAttributeSet attribs_left = new SimpleAttributeSet();
        StyleConstants.setAlignment(attribs_left, StyleConstants.ALIGN_LEFT);


        textpane.setParagraphAttributes(attribs_left, true);

        try {
            doc.insertString(0, sampleTextTop, null);
        } catch (Exception e) {
            e.printStackTrace();
        }

        textpane.setParagraphAttributes(attribs_right, true);

        try {
            doc.insertString(doc.getLength(), sampleTextBottom, null);
        } catch (Exception e) {
            e.printStackTrace();
        }

        frame.getContentPane().add(textpane);
        frame.setPreferredSize(new Dimension(370,120));
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLocationRelativeTo(null);
        frame.pack();
        frame.setVisible(true);
    }
}
