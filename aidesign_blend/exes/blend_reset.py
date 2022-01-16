""""blend reset" command executable."""

# Copyright 2022 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

import copy
import sys

from aidesign_blend.libs import defaults
from aidesign_blend.libs import utils

_argv = sys.argv
_deepcopy = copy.deepcopy
_load_json = utils.load_json
_save_json = utils.save_json
_stderr = sys.stderr

brief_usage = "blend reset"
"""Brief usage."""
usage = str(
    f"Usage: {brief_usage}\n"
    f"Help: gan help"
)
"""Usage."""

info = "Completed resetting the app data at: {}"
"""Primary info to display."""

too_many_args_info = str(
    f"\"{brief_usage}\" gets too many arguments\n"
    f"Expects 0 arguments; Gets {{}} arguments\n"
    f"{usage}"
)
"""Info to display when getting too many arguments."""

argv_copy = None
"""Consumable copy of sys.argv."""


def run():
    """Runs the executable as a command."""
    global argv_copy
    argv_copy_length = len(argv_copy)

    assert argv_copy_length >= 0

    if argv_copy_length == 0:
        # Reset blend start status
        blend_start_status = _load_json(defaults.blend_start_status_loc)
        blend_start_status["frags_path"] = None
        blend_start_status["project_path"] = None
        _save_json(blend_start_status, defaults.blend_start_status_loc)

        print(info.format(defaults.app_data_path))
        exit(0)
    else:  # elif argv_copy_length > 0:
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
