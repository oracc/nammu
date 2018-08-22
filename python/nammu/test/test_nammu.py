# -*- coding: utf-8 -*-
import pytest
import codecs
import time
import os
from python.nammu.controller.NammuController import NammuController

from java.awt import Color
from javax.swing import JSplitPane


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

    def setup_class(self):
        self.nammu = NammuController()

    def teardown_class(self):
        del self.nammu

    @pytest.mark.parametrize('text', [simpletext(), english(), arabic(),
                                      english_no_lem(), arabic_no_lem(),
                                      broken_atf()])
    def test_set_text(self, text):
        self.nammu.atfAreaController.edit_area.setText(text)
        assert self.nammu.atfAreaController.edit_area.getText() == text

    @pytest.mark.parametrize('text, caret, color', [(simpletext(), 5, black()),
                                                    (english(), 137, red()),
                                                    (arabic(), 46, pink()),
                                                    (arabic_no_lem(), 113,
                                                     blue()),
                                                    (english_no_lem(), 166,
                                                     yellow()),
                                                    (broken_atf(), 3,
                                                     green())])
    def test_syntax_highlight(self, text, caret, color):
        self.nammu.atfAreaController.edit_area.setText(text)
        # Wait here so the highlight completes before getting the styledoc
        time.sleep(2)
        doc = self.nammu.atfAreaController.edit_area.getStyledDocument()

        # Get the colour of a given character that should be highlighted
        c = doc.getForeground(doc.getCharacterElement(caret).getAttributes())
        assert c.equals(color)

    @pytest.mark.parametrize('text', [english_no_lem(), arabic_no_lem()])
    def test_successful_lem_no_existing_lem(self, text):
        self.nammu.currentFilename = 'pytest.atf'  # bypass saving the file
        self.nammu.atfAreaController.edit_area.setText(text)
        self.nammu.lemmatise()
        assert text != self.nammu.atfAreaController.edit_area.getText()

    @pytest.mark.parametrize('text', [english(), arabic()])
    def test_successful_lem_existing_lem(self, text):
        self.nammu.currentFilename = 'pytest.atf'  # bypass saving the file
        self.nammu.atfAreaController.edit_area.setText(text)
        self.nammu.lemmatise()
        assert text == self.nammu.atfAreaController.edit_area.getText()

    def test_unsuccsessful_lem(self, broken_atf):
        self.nammu.currentFilename = 'pytest.atf'  # bypass saving the file
        self.nammu.atfAreaController.edit_area.setText(broken_atf)
        self.nammu.lemmatise()

        # An empty dictionary means no validation errors
        assert self.nammu.atfAreaController.validation_errors

    @pytest.mark.parametrize('text', [english(), arabic(), english_no_lem(),
                                      arabic_no_lem()])
    def test_successful_validation(self, text):
        self.nammu.currentFilename = 'pytest.atf'  # bypass saving the file
        self.nammu.atfAreaController.edit_area.setText(text)
        self.nammu.validate()

        # An empty dictionary means no validation errors
        assert not self.nammu.atfAreaController.validation_errors

    def test_unsuccessful_validation(self, broken_atf):
        self.nammu.currentFilename = 'pytest.atf'  # bypass saving the file
        self.nammu.atfAreaController.edit_area.setText(broken_atf)
        self.nammu.validate()

        # An empty dictionary means no validation errors
        assert self.nammu.atfAreaController.validation_errors

    def test_file_load(self, monkeypatch):
        import javax.swing.JFileChooser
        monkeypatch.setattr(javax.swing.JFileChooser, 'showDialog',
                            show_diag_patch)
        monkeypatch.setattr(javax.swing.JFileChooser, 'getSelectedFile',
                            selected_file_patch_english)
        monkeypatch.setattr(self.nammu, 'handleUnsaved', unsaved_patch)

        self.nammu.openFile()
        assert len(self.nammu.atfAreaController.edit_area.getText()) > 1

    def test_saving_split_pane(self, monkeypatch, tmpdir, arabic):
        import javax.swing.JFileChooser
        monkeypatch.setattr(javax.swing.JFileChooser, 'showDialog',
                            show_diag_patch)
        monkeypatch.setattr(javax.swing.JFileChooser, 'getSelectedFile',
                            selected_file_patch_arabic)
        monkeypatch.setattr(self.nammu, 'handleUnsaved', unsaved_patch)

        self.nammu.openFile()
        self.nammu.currentFilename = str(tmpdir.join('pytest.atf'))

        self.nammu.saveFile()

        assert os.path.isfile(self.nammu.currentFilename)
        assert generic_loader(self.nammu.currentFilename) == arabic

    def test_saving_single_pane(self, monkeypatch, tmpdir, english):
        import javax.swing.JFileChooser
        monkeypatch.setattr(javax.swing.JFileChooser, 'showDialog',
                            show_diag_patch)
        monkeypatch.setattr(javax.swing.JFileChooser, 'getSelectedFile',
                            selected_file_patch_english)
        monkeypatch.setattr(self.nammu, 'handleUnsaved', unsaved_patch)

        self.nammu.openFile()
        self.nammu.currentFilename = str(tmpdir.join('pytest.atf'))

        self.nammu.saveFile()

        assert os.path.isfile(self.nammu.currentFilename)
        assert generic_loader(self.nammu.currentFilename) == english

    def test_arabic_split_pane(self, monkeypatch):

        import javax.swing.JFileChooser
        monkeypatch.setattr(javax.swing.JFileChooser, 'showDialog',
                            show_diag_patch)
        monkeypatch.setattr(javax.swing.JFileChooser, 'getSelectedFile',
                            selected_file_patch_arabic)
        monkeypatch.setattr(self.nammu, 'handleUnsaved', unsaved_patch)

        assert self.nammu.arabic_edition_on is False
        self.nammu.openFile()
        assert self.nammu.arabic_edition_on is True

        assert isinstance(self.nammu.atfAreaController.view.container,
                          JSplitPane)

    def test_edit_compound(self):
        '''
        Adding a character should trigger several edit events (insert and
        update colouring), added to the undo manager as a single edit compound
        so they are all undone/redone at once.
        '''
        pass

    def test_undo_empty_pane(self):
        '''
        Undo when empty pane should not do anything and undo stackpile should
        remain empty.
        '''
        pass

    def test_undo_after_closing_file(self):
        '''
        Undo after closing a file should not bring back the old file.
        '''
        pass

    def test_undo_edit_pane(self, simpletext):
        '''
        Check adding a simple text and undoing last edit compound works.
        '''
        pass

    def test_undo_split_primary_pane(self, simpletext):
        '''
        Using Nammu's split pane mode, check undoing something on the primary
        pane is reflected also in secondary pane.
        '''
        pass

    def test_undo_split_secondary_pane(self, simpletext):
        '''
        Using Nammu's split pane mode, check undoing something on the secondary
        pane is reflected also in primary pane.
        '''
        pass

    def test_undo_arabic_primary(self, arabic):
        '''
        Using Nammu's arabic mode, check undoing something on the primary
        pane works and arabic pane's content remains intact.
        '''
        pass

    def test_undo_arabic_pane(self, arabic):
        '''
        Using Nammu's arabic mode, check undoing something on the arabic
        pane works and primary pane's content remains intact.
        '''
        pass

# TODO Add 'redo' versions of all these cases.
#      This is stating to look like it needs its own test class.
