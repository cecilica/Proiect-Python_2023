"""This module contains constants used in the FindMissingBytes project.

The constants in this module are:
    - number_of_missing_bytes: An integer that represents the number of bytes missing from the end of a file.
        In the context of the FindMissingBytes project, this constant is used when trying to recover a corrupted
        file by guessing the missing bytes.
    - hash_format: A string that represents the format of the hash function used to verify file integrity in the
        FindMissingBytes project.
        This constant is used when comparing the hash of the recovered file to the expected hash.
"""

number_of_missing_bytes = 4
hash_format = "sha256"
