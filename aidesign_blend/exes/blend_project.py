""""blend project" command executable."""

# Copyright 2022 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

import copy
import pathlib
import sys

from os import path as ospath

from aidesign_blend.libs import defaults
from aidesign_blend.libs import utils

# Aliases

_argv = sys.argv
_deepcopy = copy.deepcopy
_exists = ospath.exists
_isabs = ospath.isabs
_isdir = ospath.isdir
_join = ospath.join
_load_json = utils.load_json
_Path = pathlib.Path
_save_json = utils.save_json
_stderr = sys.stderr

# -

brief_usage = "blend project <path-to-project>"
"""Brief usage."""

usage = str(
    f"Usage: {brief_usage}\n"
    f"Help: blend help"
)
"""Usage."""

# Nominal info strings

info = str(
    f"Selected the project at: {{}}\n"
    f"Applied the selection to \"blend start\""
)
"""Primary info to display."""

# -
# Error info strings

too_few_args_info = str(
    f"\"{brief_usage}\" gets too few arguments\n"
    f"Expects 1 arguments; Gets {{}} arguments\n"
    f"{usage}"
)
"""Info to display when getting too few arguments."""

too_many_args_info = str(
    f"\"{brief_usage}\" gets too many arguments\n"
    f"Expects 1 arguments; Gets {{}} arguments\n"
    f"{usage}"
)
"""Info to display when getting too many arguments."""

proj_does_not_exist_info = str(
    f"\"{brief_usage}\" cannot find the project\n"
    f"Please check if the project is present at: {{}}\n"
    f"{usage}"
)
"""Info to display when the selected project does not exist."""

proj_is_not_dir_info = str(
    f"\"{brief_usage}\" finds that the project is not a directory\n"
    f"Please check if the project appears as a directory at: {{}}\n"
    f"{usage}"
)
"""Info to display when the selected project is not a directory."""

# End of error info strings

argv_copy = None
"""Consumable copy of sys.argv."""


def run():
    """Runs the executable as a command."""
    global argv_copy
    argv_copy_length = len(argv_copy)

    if argv_copy_length < 1:
        print(too_few_args_info.format(argv_copy_length), file=_stderr)
        exit(1)
    elif argv_copy_length == 1:
        assert argv_copy is not None
        path_to_proj = str(argv_copy.pop(0))

        if not _isabs(path_to_proj):
            path_to_proj = _join(".", path_to_proj)

        path_to_proj = str(_Path(path_to_proj).resolve())

        if not _exists(path_to_proj):
            print(proj_does_not_exist_info.format(path_to_proj), file=_stderr)
            exit(1)

        if not _isdir(path_to_proj):
            print(proj_is_not_dir_info.format(path_to_proj), file=_stderr)
            exit(1)

        blend_start_status = _load_json(defaults.blend_start_status_loc)
        blend_start_status["project_path"] = path_to_proj
        _save_json(blend_start_status, defaults.blend_start_status_loc)

        print(info.format(path_to_proj))
        exit(0)
    else:  # elif argv_copy_length > 1:
        print(too_many_args_info.format(argv_copy_length), file=_stderr)
        exit(1)
    # end if


def main():
    """Starts the executable."""
    global argv_copy
    argv_length = len(_argv)

    assert argv_length >= 1

    argv_copy = _deepcopy(_argv)
    argv_copy.pop(0)
    run()


if __name__ == "__main__":
    main()
