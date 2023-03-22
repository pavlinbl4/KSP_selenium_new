"""
20220729 script for optimization keywords in KSP archiv
"""
# pip install beautifulsoup4
# pip install lxml
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import re
from datetime import datetime
import pyperclip
from Common.authorization import autorization
from Common.set_to_string import convert_set_to_string

red = '\033[91m'
green = '\33[32m'
end = '\033[0m'

keyword_file = '/Users/evgeniy/Documents/keywords/keywords in work.txt'


def chose_input():  # to use keywords from clip or enter your own
    keyword = pyperclip.paste()
    print(f'Do you want to use {red}{keyword}{end} as keyword?\n'
          f'Press {green}"ENTER"{end} if {green}"YES"{end} or type you keyword\n')
    answer = input()
    return answer if len(answer) > 2 else keyword


def write_keywords(final):
    with open(keyword_file, 'a') as text_file:
        text_file.write('\n')
        text_file.write(datetime.now().strftime("%Y-%m-%d") + '\n')
        final_string  = convert_set_to_string(final)
        text_file.write(final_string)


def check_keywords_number(keyword):  # take number of images from site
    try:
        images_number = browser.find_element(By.CSS_SELECTOR,
                                             'body > table:nth-child(6) > tbody:nth-child(1) > '
                                             'tr:nth-child(1) > td:nth-child(2) > table:nth-child(1) > '
                                             'tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > '
                                             'b:nth-child(1)')
    except Exception as ex:
        print(f'{red}снимков с ключевым словом {green}{keyword}{end}{red} не найденно{end}\n'
              f'program terminated')
        exit()
    images_number = images_number.text
    images_number = int(images_number.replace(' ', ''))  # удаляю возможные пробелы перед преобразованием в целое число
    print(f'{green}{images_number} снимков с ключевым словом "{keyword}"{end}')
    keyword_link = browser.current_url[:-1]
    return keyword_link, images_number


def keywords_search(keyword):  # find all my images with keyword escape KP part
    browser.find_element(By.CSS_SELECTOR, '#text').send_keys(keyword)
    browser.find_element(By.CSS_SELECTOR, '#au').send_keys('Евгений Павленко')
    browser.find_element(By.CSS_SELECTOR, '#lib0').click()
    select = Select(browser.find_element(By.NAME, 'ps'))
    select.select_by_value('100')
    browser.find_element(By.CSS_SELECTOR, '#searchbtn').click()

    return check_keywords_number(keyword)


def go_my_images(link, keyword) -> object:
    browser.get(link)
    # browser.save_screenshot(f'/Volumes/big4photo/_PYTHON/KSP_selenium/screen_shorts/{keyword} - {link[-1]}.png')
    browser.save_screenshot(f'/Users/evgeniy/Documents/keywords/{keyword} - {link[-1]}.png')
    html = browser.page_source
    return html


def get_image_links(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find_all('table')[9]
    tbody = table.find('tbody')
    images_links = tbody.find_all(title="Добавить кадрировку")
    return images_links


def get_keyword_of_image(link):
    browser.get(link)
    keywords = browser.find_element(By.ID, 'PhotoTextInfoControl1_Keywords').text
    return keywords


def keywords_opimization(keywords):
    step_1 = re.sub(
        r'(_РЕЛИГИЯ|_гипермаркеты|_фирмы|_ПРЕДМЕТ_|'
        r'_People|_ГОРОДА И СТРАНЫ_|'
        r'_PERSONS|_CITY|_ИМЯ СОБСТВЕННОЕ_|'
        r'COUNTRY|_РУССКИЙ_|'
        r'_ГОРОДА И СТРАНЫ|\|)',
        ' ',
        keywords).strip()
    step_2 = re.sub(r'\b([^\W\d_]+)(\s+\1)+\b', r'\1', re.sub(r'\W+', ' ', step_1).strip(), flags=re.I).strip()
    keywords = re.sub(r'\s+', ', ', step_2)
    return keywords


def make_text_edit_link(link):
    inner_id = re.findall(r'(?<=id=)\d+', link)[0]
    text_edit_link = f'https://image.kommersant.ru/photo/archive/adm/AddPhotoStep3.asp?ID={inner_id}&CloseForm=1'
    return text_edit_link


def select_action(keyword):
    print(f"{red}keyword {green}{keyword}{end} {red}will be used{end}\n"
          f"please make a choice:\n"
          f"1 - {red}clear all keywords{end}\n"
          f"2 - {green}optimise keywords{end}\n")
    # f"3 - enter your keywords\n")
    return int(input())


def display_your_choise(what_to_do, keyword):
    if what_to_do == 3:
        print(f'process start with keyword {green}{keyword}{end}\n')
    elif what_to_do == 2:
        print('standard keyword optimization\n')
    elif what_to_do == 1:
        print('keyword will be deleted you sure?\n')


def get_images_links(images_number, keyword_link, keyword, what_to_do):
    keywords_collection = set()
    range_number = images_number // 100 + 2  # количиство страниц выданных поиском
    for x in range(1, range_number):  # главный цикл работы программы
        link = f'{keyword_link}2&pg={x}'
        html = go_my_images(link, keyword)  # получаю html  открытой страницы
        images_links = get_image_links(html)  # получаю список ссылок редактирование изображения
        print(f'на странице {x} - {len(images_links)} снимков')

        for i in range(len(images_links)):  # (len(images_links)):
            text_edit_link = make_text_edit_link(images_links[i].get('href'))
            browser.get(text_edit_link)
            try:
                keywords = browser.find_element(By.NAME, 'KeywordsRus').text
                good_keywords = ""
                browser.find_element(By.NAME, 'KeywordsRus').clear()
                if what_to_do == 1:
                    print(f"{red} all keywords deleted{end}")
                elif what_to_do == 2:
                    good_keywords = keywords_opimization(keywords)  # прогоняем ключевые слова через оптимизатор
                    print(f"{green} keywords optimisation {end}")
                elif what_to_do == 3:
                    print("your keywords used")
                browser.find_element(By.NAME, 'KeywordsRus').send_keys(good_keywords)
                window_before = browser.window_handles[0]
                browser.find_element(By.NAME, 'Add').click()
                browser.switch_to.window(window_before)
                browser.find_element(By.NAME, 'Add').click()
                temp_set = set(good_keywords.split(', '))
                keywords_collection.update(temp_set)
                temp_set.clear()
                print(good_keywords)
                print(f'{i:40}')
            except browser:
                continue

    return keywords_collection


def main():
    # коллекция для сбора ключевых слов
    keyword = chose_input()  # keyword for work
    what_to_do = select_action(keyword)
    display_your_choise(what_to_do, keyword)
    keyword_link, images_number = keywords_search(keyword)
    keywords_collection = get_images_links(images_number, keyword_link, keyword, what_to_do)

    browser.close()
    browser.quit()
    # keywords_collection = str()
    if what_to_do > 1:
        print(keywords_collection)
        write_keywords(keywords_collection)
    else:
        print(f"{red} all keywords deleted{end}")


if __name__ == '__main__':
    browser = autorization()
    main()
    # chose_input()
    # keywords_search("слон")
    #
    # browser.close()
    # browser.quit()
