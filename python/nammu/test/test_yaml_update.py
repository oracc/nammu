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

import pytest
import os
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
