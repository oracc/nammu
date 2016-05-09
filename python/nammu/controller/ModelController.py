'''
Created on 17 Apr 2015

Displays ATF model view in a separate window.
It'll possibly be shown instead of the text view in the AtfAreaView in the 
future.

@author: raquel-ucl
'''

from java.util import Vector

from ..view.ModelView import ModelView
from pyoracc.model.translation import Translation
from pyoracc.model.ruling import Ruling
from pyoracc.model.comment import Comment
from pyoracc.model.line import Line

class ModelController(object):
    
    def __init__(self, mainControler, parsedAtf):
        """
        1. Parse text area content
        2. Change atfArea mode to model view from parent controller?
        3. Process parsed data and serialize in separate JPanel
        4. Think about whether the other user options should remain visible or
        should this just be shown in a separate window?
        """
        
        #Create view with a reference to its controller to handle events
        self.view = ModelView(self)
        
        #Will also need delegating to parent presenter
        self.controller = mainControler
        
        #Get ATF object parsed from text displated in text area
        self.atf = parsedAtf
        
        #Go through parsed ATF object, serialize and pass elements to view
        atfText = parsedAtf.text
        
        #Add a new tab in the view per object in the text
        objectID = "&" + atfText.code + " = " + atfText.description
        self.view.addObject(objectID)
        #TODO: ATF protocols are not saved in the model yet, but need to be passed here:
        #self.view.objectTab[objectID].addMetadata(objectID, atfText.project, \
        #                                          atfText.language, \
        #                                          atfText.protocols)
        self.view.addMetadata(objectID, atfText.project, \
                                                  atfText.language)

        for item in atfText.children:
            itemType = "@" + item.objecttype
            for side in item.children:
                #TODO Display side type and make panel as convenient to show all sides
                if not(isinstance(side, Translation)):
                    sideType = side.objecttype
                    #self.view.addText(objectID, itemType, sideType)
                    for line in side.children:
                        #TODO Display label and words and lemmas in dropdown boxes
                        content = Vector()
                        #TODO use polimorfism - see http://stackoverflow.com/questions/5579309/switch-instanceof
                        if (isinstance(line, Line)):
                            label = line.label
                            words = " ".join(line.words)
                            lemmas = ", ".join(line.lemmas)
                            content.clear()
                            content.add(words)
                            content.add(lemmas)
                            #content.add(translations)
                            self.view.addLine(objectID, label, content)
                        if (isinstance(line, Ruling)):
                            label = "$ ruling"
                            if line.type == "single":
                                ruling = "-------------"
                            content.clear()
                            content.add(ruling)
                            self.view.addLine(objectID, label, content)
                        if (isinstance(line, Comment)):
                            label = "# Comment"
                            comment = line.content
                            content.clear()
                            content.add(comment)
                            self.view.addLine(objectID, label, content)
                        
        
        #Display model view
        self.view.display()
        
        

        
        