"""Default values.

Not supposed to be changed but can be changed. Change if you know what you are doing.
"""

import os

_path = os.path
_join = _path.join

_curr_path = _path.dirname(__file__)
_repo_path = _path.abspath(_join(_curr_path, ".."))

default_configs_path = _join(_repo_path, "default_configs")
"""Default configs path."""
default_app_data_path = _join(default_configs_path, "app_data")
"""Default app data path."""
default_blend_project_path = _join(default_configs_path, "blend_project")
"""Default blend project path."""

app_data_path = _join(_repo_path, ".app_data")
"""App data path."""
run_status_loc = _join(app_data_path, "run_status.json")
"""Run status location."""

run_config_name = "run_config.json"
"""Run config name."""
