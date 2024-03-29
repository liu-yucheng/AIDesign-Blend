""""blend create" command executable."""

# Copyright 2022-2023 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

import copy
import pathlib
import shutil
import sys

from os import path as ospath

from aidesign_blend.libs import defaults

# Aliases

_argv = sys.argv
_copytree = shutil.copytree
_deepcopy = copy.deepcopy
_exists = ospath.exists
_exit = sys.exit
_isabs = ospath.isabs
_isdir = ospath.isdir
_join = ospath.join
_Path = pathlib.Path
_stderr = sys.stderr

# -

brief_usage = "blend create <path-to-project>"
"""Brief usage."""

usage = str(
    f"Usage: {brief_usage}\n"
    f"Help: blend help"
)
"""Usage."""

# Nominal info strings

info = f"Created a blend project at {{}}"
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

proj_exists_info = str(
    f"\"{brief_usage}\" finds that the project already exists\n"
    f"Please check the project at: {{}}\n"
    f"{usage}"
)
"""Info to display when the project to create already exists."""

proj_is_not_dir_info = str(
    f"\"{brief_usage}\" finds that the project exists but not as a directory\n"
    f"Please check the project at: {{}}\n"
    f"{usage}"
)
"""Info to display when the project exists but not as a directory."""

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
        path_to_proj = str(argv_copy.pop(0))

        if not _isabs(path_to_proj):
            path_to_proj = _join(".", path_to_proj)

        proj_exists = _exists(path_to_proj)
        proj_is_dir = _isdir(path_to_proj)

        if proj_exists and proj_is_dir:
            path_to_proj = _Path(path_to_proj).resolve()
            path_to_proj = str(path_to_proj)
            print(proj_exists_info.format(path_to_proj), file=_stderr)
            _exit(1)

        if proj_exists and (not proj_is_dir):
            path_to_proj = _Path(path_to_proj).resolve()
            path_to_proj = str(path_to_proj)
            print(proj_is_not_dir_info.format(path_to_proj), file=_stderr)
            _exit(1)

        _copytree(defaults.default_blend_project_path, path_to_proj)
        path_to_proj = _Path(path_to_proj).resolve()
        path_to_proj = str(path_to_proj)

        print(info.format(path_to_proj))
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
