"""
This module contains a class `FileChecker` that verifies if a certain file exists in a specified directory.
It uses Python's built-in `os` and `sys` libraries to perform the operations.

The module can be run as a standalone script from the command line with the directory name and file name
as arguments. If the file exists in the directory, it prints a message stating that the file exists,
otherwise it states that the file does not exist.

Usage: python file_checker.py [directory_name] [file_name]
"""

import os
import sys


class FileChecker:
    """This class checks if a file with a given name exists in a given directory."""

    dir_name = ""
    file_name = ""
    file_path = ""

    def __init__(self, dir_name, file_name):
        """Initializes the class attributes.

        Parameters
        ----------
        dir_name : str
        The name of the directory to check..
        file_name : str
        The name of the file being searched.

        Raises
        ------
        ValueError
        If the directory or file name is not valid.
        """

        # check if directory name is valid
        if not isinstance(dir_name, str) or not dir_name:
            raise ValueError("The directory name must be a non-empty string.")

        # check if file name is valid
        if not isinstance(file_name, str) or not file_name:
            raise ValueError("The file name must be a non-empty string.")

        # assign class attributes
        self.dir_name = dir_name
        self.file_name = file_name

    def check_directory(self):
        """Check if a directory exists.

        Returns
        -------
        bool
            True if the directory exists, False otherwise.
        """
        return os.path.isdir(self.dir_name)

    def check_file(self):
        """Checks if the file exists in the specified directory.

        Returns
        -------
        bool
        True if the file exists, False otherwise.
        """

        # create the absolute path of the file
        self.file_path = os.path.join(self.dir_name, self.file_name)

        # check if the file exists
        return os.path.exists(self.file_path)


if __name__ == "__main__":
    # read arguments from the command line
    args = sys.argv[1:]

    # check if there are enough arguments
    if len(args) < 2:
        print("You must specify a directory name and a file name.")
        sys.exit(1)

    # extract the directory name and file name
    directory = args[0]
    file = args[1]

    # create an instance of the FileChecker class
    fc = FileChecker(directory, file)

    # check if the directory exists
    if fc.check_directory():
        print(f"The directory {directory} exists.")
        # check if the file exists and display the result
        if fc.check_file():
            print(f"The file {file} exists in the directory {directory}.")
        else:
            print(f"The file {file} does not exist in the directory {directory}.")
    else:
        print(f"The directory {directory} does not exist.")
