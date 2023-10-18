"""Default values.

Not supposed to be changed but can be changed.
Change only if you know what you are doing.
"""

# Copyright 2022-2023 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

import pathlib

from os import path as ospath

_join = ospath.join
_Path = pathlib.Path

_libs_path = str(_Path(__file__).parent)
_main_package_path = str(_Path(_libs_path).parent)
_repo_path = str(_Path(_main_package_path).parent)

default_configs_path = _join(_repo_path, "aidesign_blend_default_configs")
"""Default configs path."""
default_app_data_path = _join(default_configs_path, "app_data")
"""Default app data path."""
default_blend_project_path = _join(default_configs_path, "blend_project")
"""Default blend project path."""
default_frags_path = _join(default_configs_path, "default_frags")
"""Default fragments path."""

app_data_path = _join(_repo_path, ".aidesign_blend_app_data")
"""App data path."""
blend_start_status_loc = _join(app_data_path, "blend_start_status.json")
"""Blend start status location."""
blenders_config_name = "blenders_config.json"
"""Blenders config name."""
