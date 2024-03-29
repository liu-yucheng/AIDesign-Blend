"""Package setup executable.

To be called by a package manager (pip or conda or others).
NOT supposed to be executed directly (via python or py).
Tells the package manager the way to install the source directory as a package.
The "entry_points" parameter of the setup function specifies the function to call when the user enters the
    corresponding command via the command line.
"""

# Copyright 2022-2023 Yucheng Liu. GNU GPL3 license.
# GNU GPL3 license copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by username: liu-yucheng
# Last updated by username: liu-yucheng

import setuptools
import shutil

from os import path as ospath

# Aliases

_copytree = shutil.copytree
_exists = ospath.exists
_find_packages = setuptools.find_packages
_setup = setuptools.setup

# End of aliases


def main():
    """Main function."""
    _setup(
        name="aidesign-blend",
        version="1.10.0",
        author="Yucheng Liu (From The AIDesign Team)",
        license="Copyright (C) 2022-2023 Yucheng Liu. GNU GPL3 license.",
        description="AIDesign image fragments blending application.",
        # ----
        packages=_find_packages(),
        entry_points={
            "console_scripts": [
                "blend = aidesign_blend.exes.blend:main"
            ]
        }  # ,
        # test_suite="aidesign_blend.tests"
    )

    # Initialize app data with the defaults if necessary
    from aidesign_blend.libs import defaults

    app_data_path = defaults.app_data_path
    default_app_data_path = defaults.default_app_data_path

    if not _exists(app_data_path):
        _copytree(default_app_data_path, app_data_path)
        print(f"Created app data at: {app_data_path}")
    else:  # elif _exists(app_data_path):
        print(f"Ensured app data at: {app_data_path}")

    # Check main command availability
    from aidesign_blend.exes import blend as _
    print("Commands available: blend")

# Top level code


if __name__ == "__main__":
    main()

# End of top level code
