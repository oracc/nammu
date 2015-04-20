'''
Created on 17 Apr 2015

Displays ATF model view in a separate window.
It'll possibly be shown instead of the text view in the AtfAreaView in the 
future.

@author: raquel-ucl
'''

from ..view.ModelView import ModelView

class ModelController():
    
    def __init__(self, mainControler):
        print "I'm the Model area controller"
        
        #Create view with a reference to its controller to handle events
        self.view = ModelView(self)
        
        #Will also need delegating to parent presenter
        self.controller = mainControler
        
        #Display model view
        self.view.display()
        
    def setModelContent(self, text):
        self.atfText = text
        
        