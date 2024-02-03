from pathlib import Path


def get_bad_words_from_txt_file(path_to_txt: str) -> str:

    with open(path_to_txt, 'r') as txt_file:
        words_to_remove = "|".join([word.strip() for word in txt_file.readlines()])
    return f"r'{words_to_remove}'"


if __name__ == '__main__':
    print(get_bad_words_from_txt_file(f'{Path.home()}/Documents/keywords/bad_words.txt'))
