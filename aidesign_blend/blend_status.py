"""The "blend status" command executable."""

# Initially added by: liu-yucheng
# Last updated by: liu-yucheng

import copy
import os
import shutil
import sys

from aidesign_blend import defaults
from aidesign_blend import utils

_brief_usage = "blend status"
_usage = str(
    "Usage: " f"{_brief_usage}" "\n"
    "Help: blend help"
)

info = str(
    "App data: {}\n"
    "\"blend start\":\n"
    "{}\n"
)
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
        if not os.path.exists(defaults.app_data_path):
            shutil.copytree(defaults.default_app_data_path, defaults.app_data_path)

        app_data_info = defaults.app_data_path
        blend_start_info = ""

        blend_start_status_dict = utils.load_json(defaults.blend_start_status_loc)

        tab_width = 4
        blend_start_lines = []
        for key in blend_start_status_dict:
            tab1 = " " * tab_width
            tab2_width = (2 * tab_width)
            tab2_width = tab2_width - len(key) % tab2_width
            tab2 = " " * tab2_width
            val = blend_start_status_dict[key]
            line = str(
                f"{tab1}" "{}:" f"{tab2}" "{}"
            ).format(
                key, val
            )
            blend_start_lines.append(line)
        # end for

        blend_start_info = "\n".join(blend_start_lines)

        print(info.format(app_data_info, blend_start_info), end="")
        exit(0)
    else:  # elif argv_copy_length > 0:
        print(too_many_args_info.format(argv_copy_length), end="")
        exit(1)
    # end if


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
