"""The "blend start" command executable."""

# Initially added by: liu-yucheng
# Last updated by: liu-yucheng


import copy
import datetime
import os
import sys
import traceback

from aidesign_blend import blenders
from aidesign_blend import defaults
from aidesign_blend import utils

_brief_usage = "blend start"
_usage = str(
    "Usage: " f"{_brief_usage}" "\n"
    "Help: gan help"
)
_timeout = 30

info = str(
    "\"" f"{_brief_usage}" "\":\n"
    "{}\n"
    "-\n"
    "Please confirm the above session setup\n"
    "Do you want to continue? [ Y (Yes) | n (no) ]: < default: Yes, timeout: " f"{_timeout}" " seconds >\n"
)
"""The primary info to display."""

will_start_session_info = str(
    "Will start a session\n"
    "---- The following will be logged to: {} ----\n"
)
"""The info to display when the session starts."""

completed_session_info = str(
    "---- The above has been logged to: {} ----\n"
    "Completed the training session\n"
)
"""The info to display when the session completes."""

aborted_session_info = "Aborted the training session\n"
"""The info to display when the user aborts the session."""

too_many_args_info = str(
    "\"" f"{_brief_usage}" "\" gets too many arguments\n"
    "Expects 0 arguments; Gets {} arguments\n"
    f"{_usage}" "\n"
)
"""The info to display when the executable gets too many arguments."""

none_frags_info = str(
    "\"" f"{_brief_usage}" "\" finds that the frags_path selection is None\n"
    "Please select the frags with the \"blend frags <path-to-frags>\" command\n"
    f"{_usage}" "\n"
)
"""The info to display when the frags selection is None."""

none_proj_info = str(
    "\"" f"{_brief_usage}" "\" finds that the project_path selection is None\n"
    "Please select a project with the \"blend project <path-to-project>\" command\n"
    f"{_usage}" "\n"
)
"""The info to display when the project selection is None."""

stopped_session_info = str(
    "---- The above has been logged to: {} ----\n"
    "Stopped the training session\n"
)
"""The info to display when the session stops from an exception."""

argv_copy = None
"""A consumable copy of sys.argv."""

frags_path = None
"""The frags path."""

proj_path = None
"""The project path."""

log_loc = None
"""The log location."""


def _start_session():
    global frags_path
    global proj_path
    global log_loc

    start_time = datetime.datetime.now()
    log_file = open(log_loc, "a+")
    all_logs = [sys.stdout, log_file]
    utils.logln(all_logs, "AIDesign-Blend session ...")
    utils.logln(all_logs, f"Project path: {proj_path}")
    utils.logln(all_logs, f"Frags path: {frags_path}")
    utils.logln(all_logs, "-")

    try:
        blender = blenders.Blender(frags_path, proj_path, all_logs, 1)
        blender.prep()
        blender.blend()
    except BaseException as base_exception:
        utils.logstr(all_logs, traceback.format_exc())
        end_time = datetime.datetime.now()
        execution_time = end_time - start_time
        utils.logln(all_logs, "-")
        utils.logln(all_logs, f"Execution stopped after: {execution_time} (days, hours: minutes: seconds)")
        utils.logln(all_logs, "... AIDesign-Blend session (stopped)")
        log_file.close()
        raise base_exception

    end_time = datetime.datetime.now()
    execution_time = end_time - start_time
    utils.logln(all_logs, "-")
    utils.logln(all_logs, f"Execution time: {execution_time} (days, hours: minutes: seconds)")
    utils.logln(all_logs, "... AIDesign-Blend session")
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
        blend_start_status = utils.load_json(defaults.blend_start_status_loc)

        frags_path = blend_start_status["frags_path"]
        proj_path = blend_start_status["project_path"]

        if frags_path is None:
            print(none_frags_info, end="")
            exit(1)
        if proj_path is None:
            print(none_proj_info, end="")
            exit(1)

        tab_width = 4
        tab1 = " " * tab_width
        blend_start_info = ""
        blend_start_lines = []
        for key in blend_start_status:
            tab2_width = 2 * tab_width
            tab2_width = tab2_width - len(key) % tab2_width
            tab2 = " " * tab2_width
            val = blend_start_status[key]
            line = str(
                f"{tab1}" "{}:" f"{tab2}" "{}"
            ).format(
                key, val
            )
            blend_start_lines.append(line)
        # end for

        blend_start_info = "\n".join(blend_start_lines)

        timed_input = utils.TimedInput()
        print(info.format(blend_start_info), end="")
        answer = timed_input.take(_timeout)

        if answer is None:
            answer = "Yes"
            print(f"\n{answer} (timeout)\n", end="")
        elif len(answer) <= 0:
            answer = "Yes"
            print(f"{answer} (default)\n", end="")

        print("-\n", end="")
        if answer.lower() == "yes" or answer.lower() == "y":
            log_loc = os.path.join(proj_path, "log.txt")
            print(will_start_session_info.format(log_loc), end="")

            try:
                _start_session()
            except BaseException as base_exception:
                exit_code = 1
                if isinstance(base_exception, SystemExit):
                    exit_code = base_exception.code
                print(stopped_session_info.format(log_loc), end="")
                exit(exit_code)
            # end try

            print(completed_session_info.format(log_loc), end="")
        else:  # elif answer.lower() == "no" or answer.lower() == "n" or ! answer is unknown !:
            print(aborted_session_info, end="")

        exit(0)
        # end if
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
