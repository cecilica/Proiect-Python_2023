import hashlib
import shutil


def create_truncated_archive(archive_name, file_name, num_bytes, hash_format="sha256"):
    """

    :param archive_name:
    :param file_name:
    :param num_bytes:
    :param hash_format:
    :return:
    """
    shutil.make_archive(archive_name, "zip", root_dir="/Users/vlungu/Desktop/test", base_dir=file_name)
    with open(archive_name + ".zip", 'rb') as file:
        content = file.read()[:-num_bytes]

    with open(archive_name + "_truncated.zip", "wb") as truncated:
        truncated.write(content)

    with open(file_name, 'rb') as file:
        content = file.read()
    file_hash = hashlib.new(hash_format, content).hexdigest()

    return archive_name + "_truncated.zip", file_name, hash_format + ":" + file_hash


print(create_truncated_archive("/Users/vlungu/Desktop/test", "/Users/vlungu/Desktop/test/test.txt", 100))

# '/Users/vlungu/Desktop/test_truncated.zip',
# '/Users/vlungu/Desktop/test/test.txt',
# 'sha256:f8ceef693a90db5930181474aafde1ea61ac7d6188e0ff7719e5c82ce187b236'
