"""Runs all the tests in the tests module or sub-package of the main package."""

# Copyright 2022-2023 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

import pathlib
import unittest

from os import path as ospath

_join = ospath.join
_Path = pathlib.Path
_TestLoader = unittest.TestLoader
_TextTestRunner = unittest.TextTestRunner

_repo_path = str(_Path(__file__).parent)
_main_package_path = _join(_repo_path, "aidesign_blend")
_tests_path = _join(_main_package_path, "tests")


def main():
    """Runs this module as an executable."""
    loader = _TestLoader()
    suite = loader.discover(start_dir=_tests_path, pattern="test*.py")
    runner = _TextTestRunner(verbosity=1)
    runner.run(test=suite)


if __name__ == "__main__":
    main()
