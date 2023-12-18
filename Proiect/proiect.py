import hashlib
import io
import multiprocessing
import zipfile
import struct

def fix_zip_file(args):
    archive_name, file_name, expected_hash = args

    with open(archive_name, 'rb') as file:
        data = file.read()
    # print(data)

    for i in range(256):
        new_data = data + bytes([i])
        # print(i, new_data)
        content = extract_and_check_hash(io.BytesIO(new_data), file_name, expected_hash)
        if content is not None:
            print(f'Success with i={i}')
            with open(f'{archive_name}_fixed.zip', 'wb') as new_file:
                new_file.write(new_data)
            return content

    print('Could not fix the zip file.')
    return None

def extract_and_check_hash(archive_data, file_name, expected_hash):
    try:
        with zipfile.ZipFile(archive_data, 'r') as archive:
            all_files = archive.namelist()
            print("Files in archive:", all_files)

            with archive.open(file_name) as file:
                content = file.read()
                file_hash = hashlib.new(expected_hash[:expected_hash.index(":")], content).hexdigest()
                if file_hash == expected_hash[expected_hash.index(":") + 1:]:
                    return content
    except (zipfile.BadZipFile, KeyError) as e:
        print(f"Caught an error: {e}")
        pass

    return None

def main():
    num_processes = 4
    pool = multiprocessing.Pool(processes=num_processes)
    arguments = [(
        '/Users/vlungu/Desktop/test_truncated.zip',
        'Users/vlungu/Desktop/test/test.txt',
        'sha256:f8ceef693a90db5930181474aafde1ea61ac7d6188e0ff7719e5c82ce187b236'
    )]

    results = pool.map(fix_zip_file, arguments)
    print(results)

    pool.close()
    pool.join()

if __name__ == "__main__":
    main()