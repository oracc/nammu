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

import filecmp
import os

import pytest

from python.nammu.controller.NammuController import NammuController
# from ..utils import update_yaml_config


@pytest.mark.skip(reason=("pyyaml is not working in the tests yet"))
def test_update_yaml_config():
    """
    Ensure that upon updating yaml settings files from jar, a users
    default project settings are not overwritten.
    """
    pth = "resources/test/"
    d = update_yaml_config(path_to_jar=pth+"jar_settings.yaml",
                           yaml_path=pth+"user_settings.yaml",
                           path_to_config=pth+"user_settings.yaml",
                           test_mode=True)
    # assert goal_setting == jar_config
    # make sure the user (project) setting is not overwritten....


def test_settings_copied_correctly(monkeypatch, tmpdir):
    """
    Check that the settings are initialised correctly at first launch.

    More specifically, this test ensures that, if the user starts Nammu without
    already having any configuration files, then local configuration files with
    the correct content will be created, without affecting the original files.

    This test currently assumes it will run on Linux/Mac.
    """
    # Mock the user's home directory
    monkeypatch.setitem(os.environ, 'HOME', str(tmpdir))
    assert os.listdir(str(tmpdir)) == []  # sanity check!
    NammuController()  # start up Nammu, but don't do anything with it
    settings_dir = os.path.join(os.environ['HOME'], '.nammu')
    for filename in ['settings.yaml', 'logging.yaml']:
        target_file = os.path.join(settings_dir, filename)
        original_file = os.path.join('resources/config', filename)
        assert os.path.isfile(target_file)
        assert filecmp.cmp(target_file, original_file)
        # Check that the original config files have not been emptied (see #347)
        with open(original_file, 'r') as orig:
            assert orig.readlines()
