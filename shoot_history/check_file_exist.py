from pathlib import Path


def create_file_if_no(path_to_folder, file_name):
    Path(f'{path_to_folder}/{file_name}').touch(exist_ok=True)
    return f'{path_to_folder}/{file_name}'


if __name__ == '__main__':
    path_to_folder = f'{Path().home()}/Documents/keywords'
    file_name = 'bad_words.txt'
    print(create_file_if_no(file_name, path_to_folder))
