import re


def get_file_extension(path_to_file):
    re_pattern = r'(?<=\.)[A-Za-z]{3,4}'
    extension = re.findall(re_pattern, path_to_file)[0]
    return extension  # string with file extension
