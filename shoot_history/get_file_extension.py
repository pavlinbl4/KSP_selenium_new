import re


def get_file_extension(path_to_file):
    re_pattern = r'(?<=\.)[1A-Za-z]{3,4}'
    extension = re.findall(re_pattern, path_to_file)[0]
    return extension  # string with file extension


if __name__ == '__main__':
    get_file_extension('/Users/evgeniy/Pictures/2023/20230613_Брега - мегалит/20230613EPAV7906.on1')