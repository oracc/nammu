import pytest
from python.nammu.controller.NammuController import NammuController


class TestNammu(object):

    def setup_class(self):
        self.nammu = NammuController()

    def teardown_class(self):
        del self.nammu

    def test_set_text(self):
        self.nammu.atfAreaController.edit_area.setText('Hello!')
        assert self.nammu.atfAreaController.edit_area.getText() == 'Hello!'

    def test_set_text2(self):
        assert 1 == 1
