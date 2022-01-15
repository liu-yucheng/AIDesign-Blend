"""The "blend project" command executable."""

# Copyright 2022 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

import copy
import os
import pathlib
import sys

from aidesign_blend.libs import defaults
from aidesign_blend.libs import utils


_brief_usage = "blend project <path-to-project>"
_usage = str(
    "Usage: " f"{_brief_usage}" "\n"
    "Help: blend help"
)

info = str(
    "Selected the project at: {}\n"
    "Applied the selection to \"blend start\""
)
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

proj_does_not_exist_info = str(
    "\"" f"{_brief_usage}" "\" cannot find the project\n"
    "Please check if the project is present at: {}\n"
    f"{_usage}" "\n"
)
"""The info to display when the selected project does not exist."""

proj_is_not_dir_info = str(
    "\"" f"{_brief_usage}" "\" finds that the project is not a directory\n"
    "Please check if the project appears as a directory at: {}\n"
    f"{_usage}" "\n"
)
"""The info to display when the selected project is not a directory."""

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
        path_to_proj = pathlib.Path(path_to_proj).resolve()
        path_to_proj = str(path_to_proj)

        if not os.path.exists(path_to_proj):
            print(proj_does_not_exist_info.format(path_to_proj), end="")
            exit(1)
        if not os.path.isdir(path_to_proj):
            print(proj_is_not_dir_info.format(path_to_proj), end="")
            exit(1)

        blend_start_status = utils.load_json(defaults.blend_start_status_loc)
        blend_start_status["project_path"] = path_to_proj
        utils.save_json(blend_start_status, defaults.blend_start_status_loc)

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
