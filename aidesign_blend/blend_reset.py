"""The "blend reset" command executable."""

# Initially added by: liu-yucheng
# Last updated by: liu-yucheng

import copy
import sys

from aidesign_blend import defaults
from aidesign_blend import utils

_brief_usage = "blend reset"
_usage = str(
    "Usage: " f"{_brief_usage}" "\n"
    "Help: gan help"
)

info = "Completed resetting the app data at: {}\n"
"""The primary info to display."""

too_many_args_info = str(
    "\"" f"{_brief_usage}" "\" gets too many arguments\n"
    "Expects 0 arguments; Gets {} arguments\n"
    f"{_usage}" "\n"
)
"""The info to display when the executable gets too many arguments."""

argv_copy = None
"""A consumable copy of sys.argv."""


def run():
    """Runs the executable as a command."""
    global argv_copy
    argv_copy_length = len(argv_copy)
    assert argv_copy_length >= 0
    if argv_copy_length == 0:
        # Reset blend start status
        blend_start_status_dict = utils.load_json(defaults.blend_start_status_loc)
        blend_start_status_dict["frags_path"] = None
        blend_start_status_dict["project_path"] = None
        utils.save_json(blend_start_status_dict, defaults.blend_start_status_loc)

        print(info.format(defaults.app_data_path), end="")
        exit(0)
    # elif argv_copy_length > 0
    else:
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
    exit(0)


# Let main be the script entry point
if __name__ == "__main__":
    main()
