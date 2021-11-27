"""The "blend" command executable."""

# Initially added by: liu-yucheng
# Last updated by: liu-yucheng

import copy
import pkg_resources
import sys


# Init _version
_version = "<unknown version>"
_packages = pkg_resources.require("aidesign-blend")
if len(_packages) > 0:
    _version = _packages[0].version

_brief_usage = "blend <command> ..."
_usage = str(
    "Usage: " f"{_brief_usage}" "\n"
    "Help: blend help"
)

info = str(
    "AIDesign-Blend (aidesign-blend) " f"{_version}" "\n"
    f"{_usage}" "\n"
)
"""The primary info to display."""

unknown_command_info = str(
    "\"" f"{_brief_usage}" "\" gets an unknown command: {}\n"
    f"{_usage}" "\n"
)
"""The info to display when the executable gets an unknown command."""

unknown_arg_info = str(
    "\"" f"{_brief_usage}" "\" gets an unknown argument: {}\n"
    f"{_usage}" "\n"
)
"""The info to display when the executable gets an unknown argument."""

argv_copy = None
"""A consumable copy of sys.argv."""


def _run_command():
    global argv_copy
    assert len(argv_copy) > 0
    command = argv_copy.pop(0)
    if len(command) <= 0:
        print(unknown_command_info.format(command), end="")
        exit(1)
    elif command[0] == "-":
        print(unknown_arg_info.format(command), end="")
        exit(1)
    elif command == "create":
        from aidesign_blend import blend_create
        blend_create.argv_copy = argv_copy
        blend_create.run()
    elif command == "status":
        from aidesign_blend import blend_status
        blend_status.argv_copy = argv_copy
        blend_status.run()
    elif command == "help":
        from aidesign_blend import blend_help
        blend_help.argv_copy = argv_copy
        blend_help.run()
    elif command == "project":
        from aidesign_blend import blend_project
        blend_project.argv_copy = argv_copy
        blend_project.run()
    elif command == "frags":
        from aidesign_blend import blend_frags
        blend_frags.argv_copy = argv_copy
        blend_frags.run()
    elif command == "reset":
        from aidesign_blend import blend_reset
        blend_reset.argv_copy = argv_copy
        blend_reset.run()
    elif command == "start":
        from aidesign_blend import blend_start
        blend_start.argv_copy = argv_copy
        blend_start.run()
    else:  # elif ! command is unknown !:
        print(unknown_command_info.format(command), end="")
        exit(1)
    # end if


def main():
    """Starts the executable."""
    global argv_copy
    argv_length = len(sys.argv)
    assert argv_length >= 1
    if argv_length == 1:
        print(info, end="")
        exit(0)
    else:  # elif argv_length > 1
        argv_copy = copy.deepcopy(sys.argv)
        argv_copy.pop(0)
        _run_command()


# Let main be the script entry point
if __name__ == '__main__':
    main()
