""""blend start" command executable."""

# Copyright 2022 Yucheng Liu. GNU GPL3 license.
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

_argv = sys.argv
_Blender = blenders.Blender
_deepcopy = copy.deepcopy
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

brief_usage = "blend start"
"""Brief usage."""
usage = str(
    f"Usage: {brief_usage}\n"
    "Help: gan help"
)
"""Usage."""
timeout = float(30)
"""Timeout."""

info = fr"""

"{brief_usage}":
{{}}
-
Please confirm the above session setup
Do you want to continue? [ Y (Yes) | n (no) ]: < default: Yes, timeout: {timeout} seconds >

"""
"""Primary info to display."""
info = info.strip()

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

    start_info = fr"""

AIDesign-Blend session
Project path: {proj_path}
Frags path: {frags_path}
-

    """
    start_info = start_info.strip()

    _logln(all_logs, start_info)

    try:
        debug_level = 1
        blender = _Blender(frags_path, proj_path, all_logs, debug_level)
        blender.prep()
        blender.blend()
    except BaseException as base_exception:
        _logstr(err_logs, _format_exc())
        end_time = _now()
        execution_time = end_time - start_time

        stop_info = fr"""

-
Execution stopped after: {execution_time} (days, hours: minutes: seconds)
End of AIDesign-Blend session (stopped)

        """
        stop_info = stop_info.strip()

        _logln(all_logs, stop_info)
        log_file.close()
        raise base_exception
    # end try

    end_time = _now()
    execution_time = end_time - start_time

    end_info = fr"""

-
Execution time: {execution_time} (days, hours: minutes: seconds)
End of AIDesign-Blend session

    """
    end_info = end_info.strip()

    _logln(all_logs, end_info)
    log_file.close()


def run():
    """Runs the executable as a command."""
    global argv_copy
    global frags_path
    global proj_path
    global log_loc
    argv_copy_length = len(argv_copy)

    assert argv_copy_length >= 0

    if argv_copy_length == 0:
        blend_start_status = _load_json(defaults.blend_start_status_loc)
        frags_path = blend_start_status["frags_path"]
        proj_path = blend_start_status["project_path"]

        if frags_path is None:
            print(none_frags_info, file=_stderr)
            exit(1)

        if proj_path is None:
            print(none_proj_info, file=_stderr)
            exit(1)

        frags_path = str(frags_path)
        proj_path = str(proj_path)

        tab_width1 = 4
        tab_width2 = 8
        tab1 = " " * tab_width1
        blend_start_lines = []
        blend_start_info = ""

        for key in blend_start_status:
            tab2 = " " * (tab_width2 - len(key) % tab_width2)
            val = blend_start_status[key]
            line = f"{tab1}{key}:{tab2}{val}"
            blend_start_lines.append(line)

        blend_start_info = "\n".join(blend_start_lines)

        timed_input = _TimedInput()
        print(info.format(blend_start_info))
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
                exit_code = 1

                if isinstance(base_exception, SystemExit):
                    exit_code = base_exception.code

                print(stopped_session_info.format(log_loc), file=_stderr)
                exit(exit_code)
            # end try

            print(completed_session_info.format(log_loc))
        else:  # elif answer.lower() == "no" or answer.lower() == "n" or answer is AnyOther:
            print(aborted_session_info)
        # end if

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
