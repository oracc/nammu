 # -*- coding: utf-8 -*-
import pytest
from python.nammu.controller.NammuController import NammuController


@pytest.fixture
def simpletext():
    return 'this is a simple test line'

@pytest.fixture
def english():
    with open('resources/test/english.atf') as f:
        return f.read()

@pytest.fixture
def english_no_lem():
    with open('resources/test/english_no_lem.atf') as f:
        return f.read()

@pytest.fixture
def broken_atf():
    with open('resources/test/english_broken.atf') as f:
        return f.read()

@pytest.fixture
def arabic():
    with open('resources/test/arabic.atf') as f:
        return f.read()

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
