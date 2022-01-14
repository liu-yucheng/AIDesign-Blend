"""The "blend frags" command executable."""

# Copyright (C) 2022 Yucheng Liu. GNU GPL Version 3.
# GNU GPL Version 3 copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by: liu-yucheng
# Last updated by: liu-yucheng

import copy
import os
import pathlib
import sys

from aidesign_blend.libs import defaults
from aidesign_blend.libs import utils


_brief_usage = "blend frags <path-to-frags>"
_usage = str(
    "Usage: " f"{_brief_usage}" "\n"
    "Help: blend help"
)

info = str(
    "Selected the frags at: {}\n"
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

frags_do_not_exist_info = str(
    "\"" f"{_brief_usage}" "\" cannot find the frags\n"
    "Please check if the frags are present at: {}\n"
    f"{_usage}" "\n"
)
"""The info to display when the selected frags do not exist."""

frags_are_not_dir_info = str(
    "\"" f"{_brief_usage}" "\" finds that the frags are not a directory\n"
    "Please check if the frags appear as a directory at: {}\n"
    f"{_usage}" "\n"
)
"""The info to display when the selected frags are not a directory."""

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
        path_to_frags = argv_copy.pop(0)
        path_to_frags = os.path.join(".", path_to_frags)
        path_to_frags = pathlib.Path(path_to_frags).resolve()
        path_to_frags = str(path_to_frags)

        if not os.path.exists(path_to_frags):
            print(frags_do_not_exist_info.format(path_to_frags), end="")
            exit(1)
        if not os.path.isdir(path_to_frags):
            print(frags_are_not_dir_info.format(path_to_frags), end="")
            exit(1)

        blend_start_status = utils.load_json(defaults.blend_start_status_loc)
        blend_start_status["frags_path"] = path_to_frags
        utils.save_json(blend_start_status, defaults.blend_start_status_loc)

        print(info.format(path_to_frags), end="")
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
