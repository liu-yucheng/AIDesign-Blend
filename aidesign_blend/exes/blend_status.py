""""blend status" command executable."""

# Copyright 2022 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

import copy
import shutil
import sys

from os import path as ospath

from aidesign_blend.libs import defaults
from aidesign_blend.libs import utils

# Aliases

_argv = sys.argv
_copytree = shutil.copytree
_deepcopy = copy.deepcopy
_exists = ospath.exists
_stderr = sys.stderr

# -

brief_usage = "blend status"
"""Brief usage."""

usage = str(
    f"Usage: {brief_usage}\n"
    f"Help: blend help"
)
"""Usage."""

# Nominal info strings

info = str(
    f"App data is at: {{}}\n"
    f"\"blend start\" status:\n"
    f"{{}}"
)
"""Primary info to display."""

# -
# Error info strings

too_many_args_info = str(
    f"\"{brief_usage}\" gets too many arguments\n"
    f"Expects 0 arguments; Gets {{}} arguments\n"
    f"{usage}"
)
"""Info to display when getting too many arguments."""

# -

argv_copy = None
"""Consumable copy of sys.argv."""


def _append_status_to_lines(status, lines, tab_width1, tab_width2):
    status: dict = status
    lines: list = lines
    tab_width1 = int(tab_width1)
    tab_width2 = int(tab_width2)

    tab1 = " " * tab_width1

    for key in status:
        key = str(key)
        key_len = len(key)

        val = status[key]
        val = str(val)

        tab_actual_width2 = tab_width2 - key_len % tab_width2
        tab2 = " " * tab_actual_width2

        line = f"{tab1}{key}:{tab2}{val}"
        lines.append(line)
    # end for


def run():
    """Runs the executable as a command."""
    global argv_copy
    argv_copy_length = len(argv_copy)

    assert argv_copy_length >= 0

    if argv_copy_length == 0:
        if not _exists(defaults.app_data_path):
            _copytree(defaults.default_app_data_path, defaults.app_data_path)

        app_data_info = defaults.app_data_path
        start_status = utils.load_json(defaults.blend_start_status_loc)

        tab_width1 = 4
        tab_width2 = 8
        start_lines = []
        _append_status_to_lines(start_status, start_lines, tab_width1, tab_width2)
        start_info = "\n".join(start_lines)
        print(info.format(app_data_info, start_info))
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
