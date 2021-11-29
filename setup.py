"""Package setup executable module.

When called by a package manager (pip/conda/python), this executable informs the package manager about how to install
the source directory as a package. The "entry_points" parameter of the setup function specifies the function to call
when the user enters the corresponding command to the command line.
"""

# Initially added by: liu-yucheng
# Last updated by: liu-yucheng

import os
import setuptools
import shutil


def main():
    setuptools.setup(
        name="aidesign-blend",
        version="0.4.0",
        description="AIDesign Image Fragments Blending Application",
        author="The AIDesign Team",
        packages=setuptools.find_packages(),
        entry_points={
            "console_scripts": [
                "blend = aidesign_blend.blend:main"
            ]
        }
        # test_suite="tests"
    )

    # Initialize app data with the defaults if necessary
    from aidesign_blend import defaults
    app_data_path = defaults.app_data_path

    if not os.path.exists(app_data_path):
        shutil.copytree(defaults.default_app_data_path, app_data_path)
    else:  # elif os.path.exists(app_data_path):
        print("App data already exists")

    print("App data is at: {}".format(app_data_path))
    print("Commands available: blend")


if __name__ == "__main__":
    main()
