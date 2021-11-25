"""The "blend" command executable."""

# Initially added by: liu-yucheng
# Last updated by: liu-yucheng

import copy
import pkg_resources
import sys

# private attributes

# Init _version
_version = "<unknown version>"
_packages = pkg_resources.require("aidesign-blend")
if len(_packages) > 0:
    _version = _packages[0].version

_brief_usage = "blend <command> ..."
_usage = str(
    "Usage: {}\n"
    "Help: blend help"
).format(_brief_usage)

# end of private attributes
# nominal info strings

info = str(
    "AIDesign-Blend (aidesign-blend) {}\n"
    "{}\n"
).format(
    _version,
    _usage
)
"""The primary info to display."""

# end of nominal info strings
# error info strings

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

# end of rror info strings
# other public attributes

argv_copy = None
"""A consumable copy of sys.argv."""

# end of other public attributes


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
    else:
        print(unknown_command_info.format(command), end="")
        exit(1)


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
