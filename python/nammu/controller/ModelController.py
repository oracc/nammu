'''
Copyright 2015 - 2018 University College London.

This file is part of Nammu.

Nammu is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Nammu is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Nammu.  If not, see <http://www.gnu.org/licenses/>.
'''

from java.util import Vector

from ..view.ModelView import ModelView
from pyoracc.model.translation import Translation
from pyoracc.model.ruling import Ruling
from pyoracc.model.comment import Comment
from pyoracc.model.line import Line
from pyoracc.model.composite import Composite


class ModelController(object):
    '''
    Displays ATF model view in a separate window.
    It'll possibly be shown instead of the text view in the AtfAreaView in the
    future.
    '''
    def __init__(self, mainControler, parsedAtf):
        """
        1. Parse text area content
        2. Change atfArea mode to model view from parent controller?
        3. Process parsed data and serialize in separate JPanel
        4. Think about whether the other user options should remain visible or
        should this just be shown in a separate window?
        """
        # Will also need delegating to parent presenter
        self.controller = mainControler

        # Load settings config:
        self.config = self.controller.config

        # Create view with a reference to its controller to handle events
        self.view = ModelView(self)

        # Get ATF object parsed from text displated in text area
        self.atf = parsedAtf

        # Shorthand for calling the logger
        self.logger = self.controller.logger

        # Go through parsed ATF object, serialize and pass elements to view
        try:
            atfText = parsedAtf.text
        except:
            atfText = None

        # Clear the console before printng any messages
        self.controller.consoleController.clearConsole()

        self.logger.info("The Model View is an experimental feature, use with "
                         "caution!")

        if isinstance(atfText, Composite) and atfText:
            self.logger.info("The current file {} contains multiple fragments "
                             "and cannot be loaded into the model view. Please"
                             " save the file as individual fragments and try "
                             " again".format(self.controller.currentFilename))
        elif atfText is None:
            self.logger.info("The current file is formatted in a way that"
                             "the model view cannot understand.")
        else:
            self.configure_model_view_single(atfText)

    def configure_model_view_single(self, atfText):
        '''
        At present the model view can only cope with files which represent a
        single fragment. This method has been moved out of init so we only
        call it if a single fragment file is loaded.
        '''

        # Add a new tab in the view per object in the text
        objectID = "&" + atfText.code + " = " + atfText.description
        self.view.addObject(objectID)
        # TODO: ATF protocols are not saved in the model yet, but need to be
        # passed here:
        # self.view.objectTab[objectID].addMetadata(objectID, atfText.project,
        #                                          atfText.language,
        #                                          atfText.protocols)
        self.view.addMetadata(objectID, atfText.project, atfText.language)

        for item in atfText.children:
            itemType = "@" + item.objecttype
            for side in item.children:
                # TODO Display side type and make panel as convenient to show
                # all sides
                if not(isinstance(side, Translation)):
                    sideType = side.objecttype
                    # self.view.addText(objectID, itemType, sideType)
                    for line in side.children:
                        # TODO Display label and words and lemmas in dropdown
                        # boxes
                        content = Vector()
                        # TODO use polimorfism - see
                        # http://stackoverflow.com/questions/5579309/switch-instanceof
                        if (isinstance(line, Line)):
                            label = line.label
                            words = " ".join(line.words)
                            lemmas = ", ".join(line.lemmas)
                            content.clear()
                            content.add(words)
                            content.add(lemmas)
                            # content.add(translations)
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

        # Display model view
        self.view.display()
