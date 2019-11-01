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

import yaml

from python.nammu.controller.NammuController import NammuController
from ..utils import get_home_env_var, update_yaml_config


def test_update_yaml_config():
    """
    Ensure that, upon updating yaml settings files from jar, a user's
    default project settings are not overwritten.
    """
    pth = "resources/test/"
    local_file = os.path.join(pth, "user_settings.yaml")
    jar_file = os.path.join(pth, "jar_settings.yaml")
    new_config = update_yaml_config(path_to_jar=jar_file,
                                    yaml_path=local_file,
                                    path_to_config=local_file,
                                    test_mode=True)
    with open(local_file, "r") as f:
        orig_config = yaml.safe_load(f)
    # Make sure the user (project) setting is not overwritten
    assert (new_config["projects"]["default"] ==
            orig_config["projects"]["default"])


def test_settings_copied_correctly(monkeypatch, tmpdir):
    """
    Check that the settings are initialised correctly at first launch.

    More specifically, this test ensures that, if the user starts Nammu without
    already having any configuration files, then local configuration files with
    the correct content will be created, without affecting the original files.
    """
    # Mock the user's home directory
    home_env_var = get_home_env_var()  # will vary depending on OS
    monkeypatch.setitem(os.environ, home_env_var, str(tmpdir))
    assert os.listdir(str(tmpdir)) == []  # sanity check!
    NammuController()  # start up Nammu, but don't do anything with it
    settings_dir = os.path.join(os.environ[home_env_var], '.nammu')
    for filename in ['settings.yaml', 'logging.yaml']:
        target_file = os.path.join(settings_dir, filename)
        original_file = os.path.join('resources', 'config', filename)
        assert os.path.isfile(target_file)
        assert filecmp.cmp(target_file, original_file)
        # Check that the original config files have not been emptied (see #347)
        with open(original_file, 'r') as orig:
            assert orig.readlines()
