""""blend frags" command executable."""

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
_exit = sys.exit
_isabs = ospath.isabs
_isdir = ospath.isdir
_join = ospath.join
_load_json = utils.load_json
_Path = pathlib.Path
_save_json = utils.save_json
_stderr = sys.stderr

# -

brief_usage = "blend frags <path-to-frags>"
"""Brief usage."""

usage = str(
    f"Usage: {brief_usage}\n"
    f"Help: blend help"
)
"""Usage."""

# Nominal info strings

info = str(
    f"Selected the frags at: {{}}\n"
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

frags_do_not_exist_info = str(
    f"\"{brief_usage}\" cannot find the frags\n"
    f"Please check if the frags are present at: {{}}\n"
    f"{usage}"
)
"""Info to display when the selected frags do not exist."""

frags_are_not_dir_info = str(
    f"\"{brief_usage}\" finds that the frags are not a directory\n"
    f"Please check if the frags appear as a directory at: {{}}\n"
    f"{usage}"
)
"""Info to display when the selected frags are not a directory."""

# End of error info strings

argv_copy = None
"""Consumable copy of sys.argv."""


def run():
    """Runs the executable as a command."""
    global argv_copy
    argv_copy_length = len(argv_copy)

    if argv_copy_length < 1:
        print(too_few_args_info.format(argv_copy_length), file=_stderr)
        _exit(1)
    elif argv_copy_length == 1:
        assert argv_copy is not None
        path_to_frags = str(argv_copy.pop(0))

        if not _isabs(path_to_frags):
            path_to_frags = _join(".", path_to_frags)

        path_to_frags = str(_Path(path_to_frags).resolve())

        if not _exists(path_to_frags):
            print(frags_do_not_exist_info.format(path_to_frags), file=_stderr)
            _exit(1)

        if not _isdir(path_to_frags):
            print(frags_are_not_dir_info.format(path_to_frags), file=_stderr)
            _exit(1)

        blend_start_status = _load_json(defaults.blend_start_status_loc)
        blend_start_status["frags_path"] = path_to_frags
        _save_json(blend_start_status, defaults.blend_start_status_loc)

        print(info.format(path_to_frags))
        _exit(0)
    else:  # elif argv_copy_length > 1:
        print(too_many_args_info.format(argv_copy_length), file=_stderr)
        _exit(1)
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
