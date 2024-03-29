""""blend start" command executable."""

# Copyright 2022-2023 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

import copy
import datetime
import sys
import traceback
import typing

from os import path as ospath

from aidesign_blend.libs import blenders
from aidesign_blend.libs import defaults
from aidesign_blend.libs import utils

# Aliases

_argv = sys.argv
_Blender = blenders.Blender
_deepcopy = copy.deepcopy
_exit = sys.exit
_format_exc = traceback.format_exc
_IO = typing.IO
_join = ospath.join
_load_json = utils.load_json
_logln = utils.logln
_logstr = utils.logstr
_now = datetime.datetime.now
_stderr = sys.stderr
_stdout = sys.stdout
_TimedInput = utils.TimedInput

# -

brief_usage = "blend start"
"""Brief usage."""

usage = str(
    f"Usage: {brief_usage}\n"
    f"Help: gan help"
)
"""Usage."""

timeout = float(30)
"""Timeout."""

# Nominal info strings

info = fr"""

"{brief_usage}":
{{}}
-
Please confirm the above session setup
Do you want to continue? [ Y (Yes) | n (no) ]: < default: Yes, timeout: {timeout} seconds >

""".strip()
"""Primary info to display."""

# -
# Error info strings

will_start_session_info = str(
    f"Will start a session\n"
    f"---- The following will be logged to: {{}} ----"
)
"""Info to display when the session starts."""

completed_session_info = str(
    f"---- The above has been logged to: {{}} ----\n"
    f"Completed the session"
)
"""Info to display when the session completes."""

aborted_session_info = "Aborted the session"
"""Info to display when the user aborts the session."""

too_many_args_info = str(
    f"\"{brief_usage}\" gets too many arguments\n"
    f"Expects 0 arguments; Gets {{}} arguments\n"
    f"{usage}"
)
"""Info to display when getting too many arguments."""

none_frags_info = str(
    f"\"{brief_usage}\" finds that the frags_path selection is None\n"
    f"Please select the frags with the \"blend frags <path-to-frags>\" command\n"
    f"{usage}"
)
"""Info to display when the frags selection is None."""

none_proj_info = str(
    f"\"{brief_usage}\" finds that the project_path selection is None\n"
    f"Please select a project with the \"blend project <path-to-project>\" command\n"
    f"{usage}"
)
"""Info to display when the project selection is None."""

stopped_session_info = str(
    f"---- The above has been logged to: {{}} ----\n"
    f"Stopped the session"
)
"""Info to display when the session stops from an exception."""

# End of error info strings
# Session info strings

session_header_info = str(
    f"AIDesign-Blend session\n"
    f"Project path: {{}}\n"
    f"Frags path: {{}}\n"
    f"-"
)
"""Session header info."""

session_stop_trailer_info = str(
    f"-\n"
    f"Execution stopped after: {{}} (days, hours: minutes: seconds)\n"
    f"End of AIDesign-Blend session (stopped)"
)
"""Session trailer info to display after execution stops."""

session_comp_trailer_info = str(
    f"-\n"
    f"Execution time: {{}} (days, hours: minutes: seconds)\n"
    f"End of AIDesign-Blend session"
)
"""Session trailer info to display after execution completes."""

# -

argv_copy = None
"""Consumable copy of sys.argv."""
frags_path = None
"""Frags path."""
proj_path = None
"""Project path."""
log_loc = None
"""Log location."""


def _start_session():
    global frags_path
    global proj_path
    global log_loc

    start_time = _now()
    log_file: _IO = open(log_loc, "a+")
    all_logs = [_stdout, log_file]
    err_logs = [_stderr, log_file]
    _logln(all_logs, session_header_info.format(proj_path, frags_path))

    try:
        debug_level = 1  # NOTE: Check before each release
        blender = _Blender(frags_path, proj_path, all_logs, debug_level)
        blender.prep()
        blender.blend()
    except BaseException as base_exception:
        _logstr(err_logs, _format_exc())
        end_time = _now()
        exe_time = end_time - start_time
        _logln(all_logs, session_stop_trailer_info.format(exe_time))
        log_file.close()
        raise base_exception
    # end try

    end_time = _now()
    exe_time = end_time - start_time
    _logln(all_logs, session_comp_trailer_info.format(exe_time))
    log_file.close()


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
    global frags_path
    global proj_path
    global log_loc
    argv_copy_length = len(argv_copy)

    assert argv_copy_length >= 0

    if argv_copy_length == 0:
        start_status = _load_json(defaults.blend_start_status_loc)
        frags_path = start_status["frags_path"]
        proj_path = start_status["project_path"]

        if frags_path is None:
            print(none_frags_info, file=_stderr)
            _exit(1)

        if proj_path is None:
            print(none_proj_info, file=_stderr)
            _exit(1)

        frags_path = str(frags_path)
        proj_path = str(proj_path)

        tab_width1 = 4
        tab_width2 = 8
        start_lines = []
        _append_status_to_lines(start_status, start_lines, tab_width1, tab_width2)
        start_info = "\n".join(start_lines)

        timed_input = _TimedInput()
        print(info.format(start_info))
        answer = timed_input.take(timeout)

        if answer is None:
            answer = "Yes"
            print(f"\n{answer} (timeout)")
        elif len(answer) <= 0:
            answer = "Yes"
            print(f"{answer} (default)")

        print("-")

        if answer.lower() == "yes" or answer.lower() == "y":
            log_loc = _join(proj_path, "log.txt")
            print(will_start_session_info.format(log_loc))

            try:
                _start_session()
            except BaseException as base_exception:
                if isinstance(base_exception, SystemExit):
                    exit_code = base_exception.code
                else:
                    exit_code = 1

                print(stopped_session_info.format(log_loc), file=_stderr)
                _exit(exit_code)
            # end try

            print(completed_session_info.format(log_loc))
        else:  # elif answer.lower() == "no" or answer.lower() == "n" or answer is AnyOther:
            print(aborted_session_info)
        # end if

        _exit(0)
    else:  # elif argv_copy_length > 0:
        print(too_many_args_info.format(argv_copy_length), file=_stderr)
        _exit(1)
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
