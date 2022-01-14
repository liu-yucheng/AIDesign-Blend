"""Package setup executable.

To be called by a package manager (pip or conda or others).
NOT supposed to be executed directly (via python or py).
Tells the package manager the way to install the source directory as a package.
The "entry_points" parameter of the setup function specifies the function to call when the user enters the
    corresponding command via the command line.
"""

# Copyright (C) 2022 Yucheng Liu. GNU GPL Version 3.
# GNU GPL Version 3 copy: https://www.gnu.org/licenses/gpl-3.0.txt
# First added by: liu-yucheng
# Last updated by: liu-yucheng

import pathlib
import setuptools
import shutil

from os import path as ospath

# Aliases

_copytree = shutil.copytree
_exists = ospath.exists
_find_packages = setuptools.find_packages
_join = ospath.join
_Path = pathlib.Path
_setup = setuptools.setup

# End of aliases


def main():
    """Main function."""
    _setup(
        name="aidesign-blend",
        version="0.9.0",
        description="AIDesign Image Fragments Blending Application",
        author="Yucheng Liu (From The AIDesign Team)",
        packages=_find_packages(),
        entry_points={
            "console_scripts": [
                "blend = aidesign_blend.exes.blend:main"
            ]
        }  # ,
        # test_suite="aidesign_blend.tests"
    )

    # Test the main command executable availability
    from aidesign_blend.exes import blend as _

    # Initialize app data with the defaults if necessary
    repo_path = str(_Path(__file__).parent)
    app_data_path = _join(repo_path, ".aidesign_blend_app_data")
    default_app_data_path = _join(repo_path, "aidesign_blend_default_configs", "app_data")

    if not _exists(app_data_path):
        _copytree(default_app_data_path, app_data_path)
        print("Created app data at: {}".format(app_data_path))
    else:  # elif _exists(app_data_path):
        print("App data already exists at: {}".format(app_data_path))

    print("Commands available: blend")

# Top level code


if __name__ == "__main__":
    main()

# End of top level code
