"""Utilities."""

# Initially added by: liu-yucheng
# Last updated by: liu-yucheng

import asyncio
import json
import sys
import threading


class TimedInput:
    """Timed input class.

    Python-native and platform-independent timed input prompt.
    """

    def __init__(self):
        """Inits self with the given args."""
        self._input_str = None
        self._subproc_code = str(
            "input_str = input()\n"
            "print(input_str)\n"
        )
        self._subproc = None

    async def _run_subproc(self):
        self._subproc = await asyncio.create_subprocess_exec(
            sys.executable, "-c", self._subproc_code, stdin=sys.stdin, stdout=asyncio.subprocess.PIPE
        )
        data = await self._subproc.stdout.readline()
        self._input_str = data.decode("utf-8", "replace").rstrip()
        await self._subproc.wait()

    def _take(self):
        self._subproc = None
        asyncio.run(self._run_subproc())

    def take(self, timeout=5.0):
        """Takes and return a input string from the user with a given timeout.

        Args:
            timeout: the timeout period length in seconds

        Returns:
            self._input_str: the taken input string, or None if there is a timeout
        """
        timeout = float(timeout)
        self._input_str = None
        thread = threading.Thread(target=self._take)
        thread.start()
        thread.join(timeout)
        if self._input_str is None and self._subproc is not None:
            self._subproc.terminate()
        return self._input_str


def load_json(from_file):
    """Loads the data from a JSON file to a dict and returns the dict.

    Args:
        from_file: the JSON file location

    Returns:
        to_dict: the dict
    """
    file = open(from_file, "r")
    to_dict = json.load(file)
    file.close()
    return to_dict


def save_json(from_dict, to_file):
    """Saves the data from a dict to a JSON file.

    Args:
        from_dict: the dict object
        to_file: the JSON file location
    """
    file = open(to_file, "w+")
    json.dump(from_dict, file, indent=4)
    file.close()
