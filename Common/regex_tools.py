import re

words_to_remove = r'_РЕЛИГИЯ|_гипермаркеты|_фирмы|_ПРЕДМЕТ_|_People|_ГОРОДА И СТРАНЫ_|_PERSONS|_CITY|_ИМЯ СОБСТВЕННОЕ_|COUNTRY|_РУССКИЙ_|_ГОРОДА И СТРАНЫ|\|'

def extract_only_words(text_string):
    if type(text_string) is list:
        text_string = ''.join(text_string)
    pattern = r'[А-Яа-яA-Za-z]+\-*[А-Яа-яA-Za-z]+'
    return re.findall(pattern, text_string)
def keywords_opimization(string):
    # remove bad words
    no_bad_words = re.sub(words_to_remove, "", string).strip()

    # remove doubles
    cleaned_string = re.sub(r'\b(\w+)\b(?=.*\b\1\b)', r'', no_bad_words)

    # Remove all punctuation except commas
    cleaned_string = re.sub(r'(?<!\w)[^\w\s,-]|[^\w\s,-](?!\w)', '', cleaned_string)

    # Extract words and separate with commas
    words = re.findall(r'\b[\w-]+\b', cleaned_string)
    result = ', '.join(words)

    # set limit of keywords
    while len(result) > 500:
        del words[-1]
        result = ', '.join(words)

    return result


def replace_to_comma(keywords: str) -> str:
    step_1 = re.sub(words_to_remove, '', keywords).strip()  # remove this words
    return re.sub(r';', ', ', step_1)


def make_text_edit_link(link):
    inner_id = re.findall(r'(?<=id=)\d+', link)[0]
    image_id = re.findall(r'(?<=photocode=)[^&]+', link)[0]
    # image_edit_link = f'https://image.kommersant.ru/photo/archive/ViewPhoto.asp?ID={inner_id}&Lang=1&L=1'
    image_edit_link = f'https://image.kommersant.ru/photo/archive/adm/AddPhotoStep3.asp?ID={inner_id}&CloseForm=1'
    return image_edit_link, image_id, inner_id


def full_shoot_html_link(shoot_id: str, page: int) -> str:  # create full shoot html link with 200 preview
    splited_soot_id = shoot_id.split('_')
    return f'https://image.kommersant.ru/photo/wp/default.aspx?shootnum={splited_soot_id[1]}' \
           f'&sourcecode={splited_soot_id[0]}&pagesize=200&previewsize=128&page={str(page)}&nl=true&ord=F'


if __name__ == '__main__':
    assert type(full_shoot_html_link('KSP_017605', 0)) == str
    print(f"{'replace_to_comma'}: {replace_to_comma('Санкт - Петербург, Петрикирхе;архитектура;религия,религия ')}")
    print(
        f"{'keywords_opimization'}: "
        f"{keywords_opimization('Санкт-Петербург, Петрикирхе;архитектура;религия, архитектура')}")
