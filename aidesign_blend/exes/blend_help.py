"""The "blend help" command executable."""

# Copyright (C) 2022 Yucheng Liu. GNU GPL Version 3.
# GNU GPL Version 3 copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by: liu-yucheng
# Last updated by: liu-yucheng

import copy
import sys

_brief_usage = "blend help"
_usage = str(
    "Usage: " f"{_brief_usage}" "\n"
    "Help: blend help"
)

info = r"""Usage: blend <command> ...
==== Commands ====
help:
    When:   You need help info. For example, now.
    How-to: blend help
create:
    When:   You create a new blend project with the defaults.
    How-to: blend create <path-to-project>
status:
    When:   You check the application status.
    How-to: blend status
project:
    When:   You select the blend project for the next session.
    How-to: blend project <path-to-project>
frags:
    When:   You select the folder of fragments for the next session.
    How-to: blend frags <path-to-frags>
start:
    When:   You start a session.
    How-to: blend start
    Notes:  You will be prompted with the command status. You need to confirm to continue.
reset:
    When:   You want to reset the app data.
    How-to: blend reset
    Notes:  You will lose the current app data after the reset.
"""
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
        print(info, end="")
        exit(0)
    else:  # elif argv_copy_length > 0:
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
