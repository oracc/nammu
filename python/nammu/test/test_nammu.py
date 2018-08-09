 # -*- coding: utf-8 -*-
import pytest
import codecs
from python.nammu.controller.NammuController import NammuController


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

class TestNammu(object):

    def setup_class(self):
        self.nammu = NammuController()

    def teardown_class(self):
        del self.nammu

    @pytest.mark.parametrize('text', [simpletext(), english(), arabic(),
                                      english_no_lem(), broken_atf()])
    def test_set_text(self, text):
        self.nammu.atfAreaController.edit_area.setText(text)
        assert self.nammu.atfAreaController.edit_area.getText() == text

    # def test_arabic_split_pane(self, arabic):
    #     assert self.nammu.arabic_edition_on == False
    #     self.nammu.atfAreaController.edit_area.setText(arabic)
    #     assert self.nammu.arabic_edition_on == True

    def test_syntax_highlight(self):
        pass

    def test_successful_lem(self):
        pass

    def test_unsuccsessful_lem(self):
        pass

    def test_saving_split_pane(self):
        pass

    @pytest.mark.parametrize('text', [english(), arabic(),
                                      english_no_lem()])
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

    def test_file_load(self):
        pass
