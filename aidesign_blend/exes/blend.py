"""The "blend" command executable."""

# Copyright 2022 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

import copy
import pkg_resources
import sys

_argv = sys.argv
_deepcopy = copy.deepcopy
_require = pkg_resources.require
_stderr = sys.stderr

# Initialize _version
_version = "<unknown version>"
_packages = _require("aidesign-blend")
if len(_packages) > 0:
    _version = _packages[0].version

brief_usage = "blend <command> ..."
"""Brief usage."""
usage = str(
    f"Usage: {brief_usage}\n"
    f"Help: blend help"
)
"""Usage."""

info = str(
    f"AIDesign-Blend (aidesign-blend) {_version}\n"
    f"{usage}"
)
"""Primary info to display."""

unknown_command_info = str(
    f"\"{brief_usage}\" gets an unknown command: {{}}\n"
    f"{usage}"
)
"""Info to display when the executable gets an unknown command."""
unknown_arg_info = str(
    f"\"{brief_usage}\" gets an unknown argument: {{}}\n"
    f"{usage}"
)
"""Info to display when the executable gets an unknown argument."""

argv_copy = None
"""Consumable copy of sys.argv."""


def _run_command():
    global argv_copy

    argv_copy = [str(elem) for elem in argv_copy]
    assert len(argv_copy) > 0
    command = argv_copy.pop(0)
    command = str(command)

    if len(command) <= 0:
        print(unknown_command_info.format(command), file=_stderr)
        exit(1)
    elif command[0] == "-":
        print(unknown_arg_info.format(command), file=_stderr)
        exit(1)
    elif command == "create":
        from aidesign_blend.exes import blend_create
        blend_create.argv_copy = argv_copy
        blend_create.run()
    elif command == "status":
        from aidesign_blend.exes import blend_status
        blend_status.argv_copy = argv_copy
        blend_status.run()
    elif command == "help":
        from aidesign_blend.exes import blend_help
        blend_help.argv_copy = argv_copy
        blend_help.run()
    elif command == "project":
        from aidesign_blend.exes import blend_project
        blend_project.argv_copy = argv_copy
        blend_project.run()
    elif command == "frags":
        from aidesign_blend.exes import blend_frags
        blend_frags.argv_copy = argv_copy
        blend_frags.run()
    elif command == "reset":
        from aidesign_blend.exes import blend_reset
        blend_reset.argv_copy = argv_copy
        blend_reset.run()
    elif command == "start":
        from aidesign_blend.exes import blend_start
        blend_start.argv_copy = argv_copy
        blend_start.run()
    else:  # elif command is AnyOther:
        print(unknown_command_info.format(command), file=_stderr)
        exit(1)
    # end if


def main():
    """Starts the executable."""
    global argv_copy
    argv_length = len(_argv)

    assert argv_length >= 1

    if argv_length == 1:
        print(info)
        exit(0)
    else:  # elif argv_length > 1:
        argv_copy = _deepcopy(_argv)
        argv_copy.pop(0)
        _run_command()


if __name__ == '__main__':
    main()
