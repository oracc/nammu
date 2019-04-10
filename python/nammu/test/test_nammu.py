# -*- coding: utf-8 -*-
import pytest
import codecs
import time
import os
from python.nammu.controller.NammuController import NammuController

from java.awt import Color
from javax.swing import JSplitPane, JFileChooser
from javax.swing.undo import CompoundEdit


@pytest.yield_fixture(scope="class", autouse=True)
def nammu():
    yield NammuController()


@pytest.fixture
def simpletext():
    return u'this is a simple test line'


@pytest.fixture
def english():
    return codecs.open('resources/test/english.atf',
                       encoding='utf-8').read()


@pytest.fixture
def english_no_lem():
    return codecs.open('resources/test/english_no_lem.atf',
                       encoding='utf-8').read()


@pytest.fixture
def broken_atf():
    return codecs.open('resources/test/english_broken.atf',
                       encoding='utf-8').read()


@pytest.fixture
def arabic():
    return codecs.open('resources/test/arabic.atf',
                       encoding='utf-8').read()


@pytest.fixture
def arabic_no_lem():
    return codecs.open('resources/test/arabic_no_lem.atf',
                       encoding='utf-8').read()


@pytest.fixture
def black():
    return Color(0, 0, 0)


@pytest.fixture
def green():
    return Color(133, 153, 0)


@pytest.fixture
def yellow():
    return Color(181, 137, 0)


@pytest.fixture
def red():
    return Color(220, 50, 47)


@pytest.fixture
def blue():
    return Color(108, 113, 196)


@pytest.fixture
def pink():
    return Color(211, 54, 130)


@pytest.fixture
def empty_compound():
    return CompoundEdit()


def show_diag_patch(a, b, c):
    '''
    Monkeypatch the clicking of the ok button on the file load dialog.
    '''
    return 0


def selected_file_patch_english(a):
    return mockFile('resources/test/english.atf')


def selected_file_patch_arabic(a):
    return mockFile('resources/test/arabic.atf')


def unsaved_patch():
    return True


def generic_loader(filename):
    return codecs.open(filename, encoding='utf-8').read()


class mockFile(object):
    '''
    A class used to monkeypatch the Java file object
    '''
    def __init__(self, filename):
        self.filename = filename

    def getCanonicalPath(self):
        return self.filename

    def getName(self):
        return os.path.basename(self.filename)


class TestNammu(object):

    @pytest.mark.parametrize('text', [simpletext(), english(), arabic(),
                                      english_no_lem(), arabic_no_lem(),
                                      broken_atf()])
    def test_set_text(self, text, nammu):
        nammu.atfAreaController.edit_area.setText(text)
        assert nammu.atfAreaController.edit_area.getText() == text

    @pytest.mark.parametrize('text, caret, color', [(simpletext(), 5, black()),
                                                    (english(), 137, red()),
                                                    (arabic(), 46, pink()),
                                                    (arabic_no_lem(), 113,
                                                     blue()),
                                                    (english_no_lem(), 166,
                                                     yellow()),
                                                    (broken_atf(), 3,
                                                     green())])
    def test_syntax_highlight(self, text, caret, color, nammu):
        nammu.atfAreaController.edit_area.setText(text)
        # Wait here so the highlight completes before getting the styledoc
        time.sleep(2)
        doc = nammu.atfAreaController.edit_area.getStyledDocument()

        # Get the colour of a given character that should be highlighted
        c = doc.getForeground(doc.getCharacterElement(caret).getAttributes())
        assert c.equals(color)

    @pytest.mark.parametrize('text', [english_no_lem(), arabic_no_lem()])
    def test_successful_lem_no_existing_lem(self, text, nammu):
        nammu.currentFilename = 'pytest.atf'  # bypass saving the file
        nammu.atfAreaController.edit_area.setText(text)
        nammu.lemmatise()
        assert text != nammu.atfAreaController.edit_area.getText()

    @pytest.mark.parametrize('text', [english(), arabic()])
    def test_successful_lem_existing_lem(self, text, nammu):
        nammu.currentFilename = 'pytest.atf'  # bypass saving the file
        nammu.atfAreaController.edit_area.setText(text)
        nammu.lemmatise()
        assert text == nammu.atfAreaController.edit_area.getText()

    def test_unsuccsessful_lem(self, broken_atf, nammu):
        nammu.currentFilename = 'pytest.atf'  # bypass saving the file
        nammu.atfAreaController.edit_area.setText(broken_atf)
        nammu.lemmatise()

        # An empty dictionary means no validation errors
        assert nammu.atfAreaController.validation_errors

    @pytest.mark.parametrize('text', [english(), arabic(), english_no_lem(),
                                      arabic_no_lem()])
    def test_successful_validation(self, text, nammu):
        nammu.currentFilename = 'pytest.atf'  # bypass saving the file
        nammu.atfAreaController.edit_area.setText(text)
        nammu.validate()

        # An empty dictionary means no validation errors
        assert not nammu.atfAreaController.validation_errors

    def test_unsuccessful_validation(self, broken_atf, nammu):
        nammu.currentFilename = 'pytest.atf'  # bypass saving the file
        nammu.atfAreaController.edit_area.setText(broken_atf)
        nammu.validate()

        # An empty dictionary means no validation errors
        assert nammu.atfAreaController.validation_errors

    def test_file_load(self, monkeypatch, nammu):
        monkeypatch.setattr(JFileChooser, 'showDialog',
                            show_diag_patch)
        monkeypatch.setattr(JFileChooser, 'getSelectedFile',
                            selected_file_patch_english)
        monkeypatch.setattr(nammu, 'handleUnsaved', unsaved_patch)

        nammu.openFile()
        assert len(nammu.atfAreaController.edit_area.getText()) > 1

    def test_saving_split_pane(self, monkeypatch, tmpdir, arabic, nammu):
        monkeypatch.setattr(JFileChooser, 'showDialog',
                            show_diag_patch)
        monkeypatch.setattr(JFileChooser, 'getSelectedFile',
                            selected_file_patch_arabic)
        monkeypatch.setattr(nammu, 'handleUnsaved', unsaved_patch)

        nammu.openFile()
        nammu.currentFilename = str(tmpdir.join('pytest.atf'))

        nammu.saveFile()

        assert os.path.isfile(nammu.currentFilename)
        assert generic_loader(nammu.currentFilename) == arabic

    def test_saving_single_pane(self, monkeypatch, tmpdir, english, nammu):
        monkeypatch.setattr(JFileChooser, 'showDialog',
                            show_diag_patch)
        monkeypatch.setattr(JFileChooser, 'getSelectedFile',
                            selected_file_patch_english)
        monkeypatch.setattr(nammu, 'handleUnsaved', unsaved_patch)

        nammu.openFile()
        nammu.currentFilename = str(tmpdir.join('pytest.atf'))

        nammu.saveFile()

        assert os.path.isfile(nammu.currentFilename)
        assert generic_loader(nammu.currentFilename) == english

    def test_arabic_split_pane(self, monkeypatch, nammu):
        monkeypatch.setattr(JFileChooser, 'showDialog',
                            show_diag_patch)
        monkeypatch.setattr(JFileChooser, 'getSelectedFile',
                            selected_file_patch_arabic)
        monkeypatch.setattr(nammu, 'handleUnsaved', unsaved_patch)

        assert nammu.arabic_edition_on is False
        nammu.openFile()
        assert nammu.arabic_edition_on is True

        assert isinstance(nammu.atfAreaController.view.container,
                          JSplitPane)

    def test_edit_compound(self, nammu):
        '''
        Adding a character should trigger several edit events (insert and
        update colouring), added to the undo manager as a single edit compound
        so they are all undone/redone at once.
        '''
        controller = nammu.atfAreaController
        controller.edit_area.setText("a")
        listener = controller.view.edit_listener
        # Edits list within the undo_manager is not accessible and toString()
        # is the only way I found to inspect it.
        # TODO: I could do some of this stuff in Java, where I can access the
        # edits, but that's a bit overcomplicated at this stage.
        assert ("edits: []" not in controller.undo_manager.toString())

    def test_undo_empty_pane(self, nammu):
        '''
        Undo when empty pane should not do anything and the undo stackpile
        should remain empty.
        This test is needed because undoing empty panels is unstable and
        sometimes raises exceptions.
        '''
        controller = nammu.atfAreaController
        controller.clearAtfArea()
        controller.undo()
        assert ("edits: []" in controller.undo_manager.toString())

    def test_redo_empty_pane(self, nammu):
        '''
        Redo when empty pane should not do anything and the undo stackpile
        should remain empty.
        This test is needed because undoing empty panels is unstable and
        sometimes raises exceptions.
        '''
        controller = nammu.atfAreaController
        controller.clearAtfArea()
        controller.redo()
        assert ("edits: []" in controller.undo_manager.toString())

    def test_undo_after_opening_file(self, monkeypatch, nammu):
        '''
        Undo after opening a new file should not bring back the old file.
        '''
        monkeypatch.setattr(JFileChooser, 'showDialog',
                            show_diag_patch)
        monkeypatch.setattr(JFileChooser, 'getSelectedFile',
                            selected_file_patch_english)
        monkeypatch.setattr(nammu, 'handleUnsaved', unsaved_patch)
        nammu.openFile()
        controller = nammu.atfAreaController
        controller.undo()
        assert ("edits: []" in controller.undo_manager.toString())

    def test_undo_after_closing_file(self, monkeypatch, nammu):
        '''
        Undo after closing a file should not bring back the old file.
        '''
        monkeypatch.setattr(JFileChooser, 'showDialog',
                            show_diag_patch)
        monkeypatch.setattr(JFileChooser, 'getSelectedFile',
                            selected_file_patch_english)
        monkeypatch.setattr(nammu, 'handleUnsaved', unsaved_patch)
        nammu.openFile()
        nammu.closeFile()
        controller = nammu.atfAreaController
        controller.undo()
        assert ("edits: []" in controller.undo_manager.toString())

    def test_undo_edit_pane(self, empty_compound, nammu):
        '''
        Check adding a simple text and undoing last edit compound works.
        '''
        controller = nammu.atfAreaController
        undo_manager = controller.undo_manager
        # Clear all possible edits from previous tests
        undo_manager.discardAllEdits()
        # Write something to undo
        controller.edit_area.setText("Hello Nammu!")
        controller.undo()
        assert (controller.edit_area.getText() == "" and
                "edits: []" not in undo_manager.toString())

    def test_undo_split_primary_pane(self, simpletext, nammu):
        '''
        Using Nammu's split pane mode, check undoing something on the primary
        pane is reflected also in secondary pane and vice versa.
        Undo action is not linked to an edit area but to the controller, so
        this test checks for undoing in both primary and secondary.
        '''
        controller = nammu.atfAreaController
        nammu.splitEditorV()
        controller.edit_area.setText("Hello primary edit area!")
        controller.undo()
        assert (controller.edit_area.getText() ==
                controller.secondary_area.getText())

    def test_redo_split_primary_pane(self, simpletext, nammu):
        '''
        Using Nammu's split pane mode, check redoing something on the primary
        pane is reflected also in secondary pane and vice versa.
        Redo action is not linked to an edit area but to the controller, so
        this test checks for redoing in both primary and secondary.
        '''
        controller = nammu.atfAreaController
        nammu.splitEditorV()
        controller.edit_area.setText("Hello primary edit area!")
        controller.undo()
        controller.redo()
        assert (controller.edit_area.getText() ==
                controller.secondary_area.getText())

    def test_undo_arabic_primary(self, arabic, nammu):
        '''
        Using Nammu's arabic mode, check undoing something on the primary
        pane works and arabic pane's content remains intact.
        '''
        controller = nammu.atfAreaController
        nammu.arabic()
        controller.edit_area.setText("Hello primary edit area!")
        controller.arabic_area.setText("في شتة")
        controller.undo()
        assert (controller.edit_area.getText() == "Hello primary edit area!"
                and controller.arabic_area.getText() == "")

    def test_redo_arabic_primary(self, arabic, nammu):
        '''
        Using Nammu's arabic mode, check redoing something on the primary
        pane works and arabic pane's content remains intact.
        '''
        controller = nammu.atfAreaController
        nammu.arabic()
        controller.edit_area.setText("Hello primary edit area!")
        controller.arabic_area.setText("في شتة")
        controller.undo()
        controller.redo()
        assert (controller.edit_area.getText() == "Hello primary edit area!"
                and controller.arabic_area.getText() == "في شتة")

    def test_undo_arabic_pane(self, arabic, nammu):
        '''
        Using Nammu's arabic mode, check undoing something on the arabic
        pane works and primary pane's content remains intact.
        '''
        controller = nammu.atfAreaController
        nammu.arabic()
        controller.arabic_area.setText("في شتة")
        controller.edit_area.setText("Hello primary edit area!")
        controller.undo()
        assert (controller.edit_area.getText() == ""
                and controller.arabic_area.getText() == "في شتة")

    def test_redo_arabic_pane(self, arabic, nammu):
        '''
        Using Nammu's arabic mode, check redoing something on the arabic
        pane works and primary pane's content remains intact.
        '''
        controller = nammu.atfAreaController
        nammu.arabic()
        controller.arabic_area.setText("في شتة")
        controller.edit_area.setText("Hello primary edit area!")
        controller.undo()
        controller.redo()
        assert (controller.edit_area.getText() == "Hello primary edit area!"
                and controller.arabic_area.getText() == "في شتة")
