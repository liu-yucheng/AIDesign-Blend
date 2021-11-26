"""The "blend create" command executable."""

# Initially added by: liu-yucheng
# Last updated by: liu-yucheng

import copy
import os
import pathlib
import shutil
import sys

from aidesign_blend import defaults

_Path = pathlib.Path


_brief_usage = "blend create <path-to-project>"
_usage = str(
    "Usage: " f"{_brief_usage}" "\n"
    "Help: blend help"
)

info = "Created a blend project at {}\n"
"""The primary info to display."""

too_few_args_info = str(
    "\"" f"{_brief_usage}" "\" gets too few arguments\n"
    "Expects 1 arguments; Gets {} arguments\n"
    f"{_usage}" "\n"
)
"""The info to display when the executable gets too few arguments."""

too_many_args_info = str(
    "\"" f"{_brief_usage}" "\" gets too many arguments\n"
    "Expects 1 arguments; Gets {} arguments\n"
    f"{_usage}" "\n"
)
"""The info to display when the executable gets too many arguments."""

proj_exists_info = str(
    "\"" f"{_brief_usage}" "\" finds that the project already exists\n"
    "Please check the project at: {}\n"
    f"{_usage}" "\n"
)
"""The info to display when the project to create already exists."""

proj_is_not_dir_info = str(
    "\"" f"{_brief_usage}" "\" finds that the project exists but not as a directory\n"
    "Please check the project at: {}\n"
    f"{_usage}" "\n"
)
"""The info to display when the project exists but not as a directory."""

argv_copy = None
"""A consumable copy of sys.argv."""


def run():
    """Runs the executable as a command."""
    global argv_copy
    argv_copy_length = len(argv_copy)
    assert argv_copy_length >= 0
    if argv_copy_length < 1:
        print(too_few_args_info.format(argv_copy_length), end="")
        exit(1)
    elif argv_copy_length == 1:
        path_to_proj = argv_copy.pop(0)
        path_to_proj = os.path.join(".", path_to_proj)

        proj_exists = os.path.exists(path_to_proj)
        proj_is_dir = os.path.isdir(path_to_proj)
        if proj_exists and proj_is_dir:
            path_to_proj = _Path(path_to_proj).resolve()
            path_to_proj = str(path_to_proj)
            print(proj_exists_info.format(path_to_proj), end="")
            exit(1)
        if proj_exists and (not proj_is_dir):
            path_to_proj = _Path(path_to_proj).resolve()
            path_to_proj = str(path_to_proj)
            print(proj_is_not_dir_info.format(path_to_proj), end="")
            exit(1)

        shutil.copytree(defaults.default_blend_project_path, path_to_proj)
        path_to_proj = _Path(path_to_proj).resolve()
        path_to_proj = str(path_to_proj)

        print(info.format(path_to_proj), end="")
        exit(0)
    else:  # elif argv_copy_length > 1:
        print(too_many_args_info.format(argv_copy_length), end="")
        exit(1)


def main():
    """Starts the executable."""
    global argv_copy
    argv_length = len(sys.argv)
    assert argv_length >= 1
    argv_copy = copy.deepcopy(sys.argv)
    argv_copy.pop(0)
    run()


# Let main be the script entry point
if __name__ == "__main__":
    main()
