'''
Created on 25 Mar 2014

@author: jamespjh
'''

from javax.swing import *
from javax.swing.event import DocumentListener
from java.awt import BorderLayout, GridLayout, Color, Dimension
from javax.swing.border import BevelBorder
from java.lang import Short


from org.kohsuke.github import GitHub

gh=GitHub.connect()
me=gh.getMyself()
this_repo=gh.getRepository("jamespjh/nammu")

frame = JFrame('ORACC Editor Prototype 0.0.1, (Codename Nammu)',
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE,
            size = (1000, 1000)
            
        )
tabber=JTabbedPane()

object_view=JPanel()
object_view.layout=BoxLayout(object_view,BoxLayout.PAGE_AXIS)
object_view.visible=False

def MakeObjectView(content):
    object_model=JPanel(border=BorderFactory.createBevelBorder(BevelBorder.RAISED))
    object_model.layout=BoxLayout(object_model,BoxLayout.PAGE_AXIS)
    lines=content.split("\n")
    title=lines[0]
    object_model.add(JLabel(title))
    for line in lines[1:]:
        line_pane=JPanel(border=BorderFactory.createLineBorder(Color.black))
        data=line.split(":")
        if len(data)==2:
            key,value=data
            line_pane.add(JLabel(key+":"))
            line_pane.add(JTextField(value))
        object_model.add(line_pane)
        line_pane.maximumSize=Dimension(Short.MAX_VALUE,line_pane.preferredSize.height)
    return object_model

def updater(text):
    for component in object_view.components:
        object_view.remove(component)

    for para in text.split("\n\n"):
        object_view.add(MakeObjectView(para))
    object_view.revalidate()
    object_view.repaint()

class ParagraphListener(DocumentListener):
    def removeUpdate(self,event):
        doc=event.document
        text=doc.getText(0,doc.endPosition.offset)
        updater(text)
        
    def insertUpdate(self,event):
        doc=event.document
        text=doc.getText(0,doc.endPosition.offset)
        updater(text)
    


editor=JEditorPane()
editor.text=this_repo.getFileContent("resources/dummy.txt").content
updater(editor.text)

editor.document.documentListener=ParagraphListener()
scroller = JScrollPane(editor,
                       verticalScrollBarPolicy=JScrollPane.VERTICAL_SCROLLBAR_ALWAYS,);




tabber.addTab("Text View", None, scroller)
tabber.addTab("Model View", None, object_view)
frame.add(tabber)

def main():
    frame.visible = True
    
if __name__ == '__main__':
    main()