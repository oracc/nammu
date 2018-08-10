 # -*- coding: utf-8 -*-
import pytest
import codecs
import time
from python.nammu.controller.NammuController import NammuController

from java.awt import Color


@pytest.fixture
def simpletext():
    return u'this is a simple test line'

@pytest.fixture
def english():
    return codecs.open('resources/test/english.atf', encoding='utf-8').read()

@pytest.fixture
def english_no_lem():
    return codecs.open('resources/test/english_no_lem.atf', encoding='utf-8').read()

@pytest.fixture
def broken_atf():
    return codecs.open('resources/test/english_broken.atf', encoding='utf-8').read()

@pytest.fixture
def arabic():
    return codecs.open('resources/test/arabic.atf', encoding='utf-8').read()

@pytest.fixture
def arabic_no_lem():
    return codecs.open('resources/test/arabic_no_lem.atf', encoding='utf-8').read()

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
                                                    (arabic_no_lem(), 113, blue()),
                                                    (english_no_lem(), 166, yellow()),
                                                    (broken_atf(), 3, green())])
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

    # def test_file_load(self):
    #     pass
    #
    # def test_saving_split_pane(self):
    #     pass
    #
    # def test_saving_single_pane(self):
    #     pass

    # def test_arabic_split_pane(self, arabic):
    #     assert self.nammu.arabic_edition_on == False
    #     self.nammu.atfAreaController.edit_area.setText(arabic)
    #     assert self.nammu.arabic_edition_on == True
