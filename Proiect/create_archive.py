"""
This module contains a function to create a truncated archive from a given file by removing a specified
number of bytes from the end of the original file. It also computes the hash of the specified file.

The module uses the `FileChecker` class from the `input_data` module to verify if a certain file
exists in a specified directory before creating the truncated archive.

The module can be run as a standalone script. When run as a script, it expects four command-line
arguments in the following order:
    1. The name of the archive to be created.
    2. The name of the file to be truncated and added to the archive.
    3. The number of bytes to be removed from the end of the original file.
    4. The hash format to be used (optional, default is "sha256").

The script prints a tuple that contains the name of the truncated archive, the file name, and the hash of the file.

Usage: python script.py [archive_name] [file_name] [num_bytes] [hash_format]
"""

import hashlib
import shutil
import sys
import constants as const
from input_data import FileChecker


def create_truncated_archive(archive_name, file_name, num_bytes, hash_format="sha256"):
    """
    This function creates a truncated archive by removing a specified number of bytes from the end of the original file,
    and it also computes the hash of the specified file.

    :param archive_name: The name of the archive file to be created.
    :param file_name: The name of the file to be added to the archive.
    :param num_bytes: The number of bytes to be removed from the end of the original file.
    :param hash_format: The hash format to be used. Default is "sha256".
    :return: A tuple that contains the name of the truncated archive, the file name, and the hash of the file.
    """

    # Instantiate the FileChecker class
    fc = FileChecker(archive_name, file_name)

    # Check if the directory exists
    if not fc.check_directory():
        raise FileNotFoundError(f"The directory does not exist: {archive_name}")

    # Check if the file exists in the directory
    if not fc.check_file():
        raise FileNotFoundError(f"The file does not exist: {file_name}")

    # Create an archive of the directory
    shutil.make_archive(archive_name, "zip", root_dir=archive_name, base_dir=file_name)

    with open(archive_name + ".zip", 'rb') as file:
        content = file.read()
    print(content)

    # Open the created archive and read its content
    with open(archive_name + ".zip", 'rb') as file:
        # Remove the specified number of bytes from the end of the file content
        content = file.read()[:-num_bytes]

    # Write the truncated content to a new archive
    with open(archive_name + "_truncated.zip", "wb") as truncated:
        truncated.write(content)

    # Open the original file and compute its hash
    with open(fc.file_path, 'rb') as file:
        content = file.read()
    file_hash = hashlib.new(hash_format, content).hexdigest()

    # Return the name of the truncated archive, the file name, and the hash of the file
    return archive_name + "_truncated.zip", file_name, file_hash


def main():
    # Check command-line arguments
    if len(sys.argv) < 5:
        print("Usage: python script.py [archive_name] [file_name] [num_bytes] [hash_format]")
        sys.exit(1)

    # Parse command-line arguments
    archive_name = sys.argv[1]
    file_name = sys.argv[2]
    num_bytes = const.number_of_missing_bytes
    hash_format = const.hash_format

    # Call the function
    result = create_truncated_archive(archive_name, file_name, num_bytes, hash_format)

    # Print the result
    print(result)


if __name__ == "__main__":
    main()
