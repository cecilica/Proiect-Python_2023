import hashlib
import io
import itertools
import multiprocessing
import zipfile
import sys
import constants as const


def fix_zip_file(args):
    """
    Attempt to fix a truncated archive by trying all possible combinations of missing bytes.

    :param args: A tuple containing the name of the archive to be fixed,
                 the name of the file expected in the archive, and the expected hash of the file.
    :return: The content of the file if the archive is successfully fixed, else None.
    """
    # Unpack arguments
    archive_name, file_name, expected_hash = args

    # Open the archive and read its content
    with open(archive_name, 'rb') as file:
        data = file.read()

    # Generate all combinations of 5 bytes
    for byte_values in itertools.product(range(256), repeat=const.number_of_missing_bytes):
        new_data = data + bytes(byte_values)

        # Try to extract the file from the archive and check its hash
        content = extract_and_check_hash(io.BytesIO(new_data), file_name, expected_hash)
        if content is not None:
            print(f'Success with {byte_values}')

            # Write the fixed archive to a new file
            with open(f'{archive_name}_fixed.zip', 'wb') as new_file:
                new_file.write(new_data)
            return content
        print(f'Error with {byte_values}.')

    print('Could not fix the zip file.')
    return None


def extract_and_check_hash(archive_data, file_name, expected_hash):
    """
    Extract a file from a zip archive and check its hash.

    :param archive_data: A file-like object representing a zip archive.
    :param file_name: The name of the file to be extracted from the archive.
    :param expected_hash: The expected hash of the file.
    :return: The content of the file if the hash matches the expected hash, else None.
    """
    # Extract the file from the archive and check its hash
    try:
        with zipfile.ZipFile(archive_data, 'r') as archive:
            all_files = archive.namelist()
            print("Files in archive:", all_files)

            with archive.open(file_name) as file:
                content = file.read()
                file_hash = hashlib.new(expected_hash[:expected_hash.index(":")], content).hexdigest()
                if file_hash == expected_hash[expected_hash.index(":") + 1:]:
                    return content
    except (zipfile.BadZipFile, KeyError, ValueError) as e:
        print(f"Caught an error: {e}")
        pass

    return None


def main():
    """
    The main function of the script. It parses command-line arguments and calls the fix_zip_file function.
    """
    # Check command-line arguments
    if len(sys.argv) < 4:
        print("Usage: python script.py [archive_name] [file_name] [expected_hash]")
        sys.exit(1)

    # Parse command-line arguments
    archive_name = sys.argv[1]
    file_name = sys.argv[2]
    expected_hash = sys.argv[3]

    # Prepare arguments for the fix_zip_file function
    arguments = [(archive_name, file_name, expected_hash)]

    # Create a multiprocessing pool
    num_processes = 10
    pool = multiprocessing.Pool(processes=num_processes)

    # Call the fix_zip_file function with the arguments
    results = pool.map(fix_zip_file, arguments)
    print(results)

    pool.close()
    pool.join()


if __name__ == "__main__":
    main()
