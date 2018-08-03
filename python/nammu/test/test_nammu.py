import pytest
from python.nammu.controller.NammuController import NammuController



class TestNammu(object):

    def setup_method(self, method):
        self.nammu = NammuController()

    def teardown_method(self, method):
        self.nammu.quit()

    def test_set_text(self):
        self.nammu.atfAreaController.edit_area.setText('Hello!')
        assert self.nammu.atfAreaController.edit_area.getText() == 'Hello!'
