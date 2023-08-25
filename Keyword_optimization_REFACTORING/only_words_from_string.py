import re


def extract_words_no_digits(text_string):
    if type(text_string) is list:
        text_string = ''.join(text_string)
    pattern = r'[А-Яа-яA-Za-z]+\-*[А-Яа-яA-Za-z]+'
    return re.findall(pattern, text_string)


if __name__ == '__main__':
    print(
        extract_words_no_digits(
            'beautifulsoup42023-03-22конюшенный,, 2023,, petersburg,, ,, saint,, пассажир, wi-fi, канал,, инвентарь, it'))
