"""Default values.

Not supposed to be changed but can be changed. Change if you know what you are doing.
"""

# Copyright (C) 2022 Yucheng Liu. GNU GPL Version 3.
# GNU GPL Version 3 copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by: liu-yucheng
# Last updated by: liu-yucheng

import pathlib

from os import path as ospath

_join = ospath.join
_Path = pathlib.Path

_curr_path = str(_Path(__file__).parent)
_libs_path = str(_Path(_curr_path).parent)
_repo_path = str(_Path(_libs_path).parent)

default_configs_path = _join(_repo_path, "aidesign_blend_default_configs")
"""Default configs path."""
default_app_data_path = _join(default_configs_path, "app_data")
"""Default app data path."""
default_blend_project_path = _join(default_configs_path, "blend_project")
"""Default blend project path."""
default_frags_path = _join(default_configs_path, "default_frags")
"""Default fragments path"""

app_data_path = _join(_repo_path, ".aidesign_blend_app_data")
"""App data path."""
blend_start_status_loc = _join(app_data_path, "blend_start_status.json")
"""Blend start status location."""
blenders_config_name = "blenders_config.json"
"""Blenders config name."""
