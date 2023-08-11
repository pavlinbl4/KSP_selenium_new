"""
20220729 script for optimization keywords in KSP archiv
"""
import time

# pip install beautifulsoup4
# pip install lxml
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import re
import pyperclip
from Common.authorization import autorization
from Keyword_optimization_REFACTORING.add_some_keywords import add_new_keywords
from Keyword_optimization_REFACTORING.keywords_in_txt_file import write_keywords_in_txt_file
from Keyword_optimization_REFACTORING.make_better import keywords_opimization
from Keyword_optimization_REFACTORING.remove_wrong_keyword import remove_mistake
import logging

from Keyword_optimization_REFACTORING.user_communication import display_your_choice

red = '\033[91m'
green = '\33[32m'
end = '\033[0m'



def chose_input():  # to use keywords from clip or enter your own
    keyword = pyperclip.paste()
    print(f'Do you want to use {red}{keyword}{end} as keyword?\n'
          f'Press {green}"ENTER"{end} if {green}"YES"{end} or type you keyword\n')
    answer = input()
    return answer if len(answer) > 2 else keyword


def check_keywords_number(keyword):  # take number of images from site
    try:
        images_number = driver.find_element(By.CSS_SELECTOR,
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
    keyword_link = driver.current_url[:-1]
    return keyword_link, images_number


def keywords_search(keyword):  # find all my images with keyword escape KP part
    driver.find_element(By.CSS_SELECTOR, '#text').send_keys(keyword)
    driver.find_element(By.CSS_SELECTOR, '#au').send_keys('Евгений Павленко')
    driver.find_element(By.CSS_SELECTOR, '#lib0').click()
    select = Select(driver.find_element(By.NAME, 'ps'))
    select.select_by_value('100')
    driver.find_element(By.CSS_SELECTOR, '#searchbtn').click()

    return check_keywords_number(keyword)


def go_my_images(link, keyword) -> object:
    driver.get(link)
    # browser.save_screenshot(f'/Volumes/big4photo/_PYTHON/KSP_selenium/screen_shorts/{keyword} - {link[-1]}.png')
    driver.save_screenshot(f'/Users/evgeniy/Documents/keywords/{keyword} - {link[-1]}.png')
    html = driver.page_source
    return html


def get_image_links(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find_all('table')[9]
    tbody = table.find('tbody')
    images_links = tbody.find_all(title="Добавить кадрировку")
    return images_links


def get_keyword_of_image(link):
    driver.get(link)
    keywords = driver.find_element(By.ID, 'PhotoTextInfoControl1_Keywords').text
    return keywords


def make_text_edit_link(link):
    inner_id = re.findall(r'(?<=id=)\d+', link)[0]
    text_edit_link = f'https://image.kommersant.ru/photo/archive/adm/AddPhotoStep3.asp?ID={inner_id}&CloseForm=1'
    return text_edit_link


def select_action(keyword):
    print(f"{red}keyword {green}{keyword}{end} {red}will be used{end}\n"
          f"please make a choice:\n"
          f"1 - {red}clear all keywords{end}\n"
          f"2 - {green}optimise keywords{end}\n"
          f"3 - {green}remove wrong keyword{end}\n"
          f'4 - {green}and keywords collection to images{end}\n')
    return int(input())





def set_keywords_to_site(good_keywords):
    driver.find_element(By.NAME, 'KeywordsRus').send_keys(good_keywords)
    driver.find_element(By.NAME, 'Add').click()


def get_images_links(images_number, keyword_link, keyword, what_to_do, new_keywords):
    keywords_collection = set()
    range_number = images_number // 100 + 2  # количиство страниц выданных поиском
    for x in range(1, range_number):  # главный цикл работы программы
        link = f'{keyword_link}2&pg={x}'
        html = go_my_images(link, keyword)  # получаю html  открытой страницы
        images_links = get_image_links(html)  # получаю список ссылок редактирование изображения
        print(f'на странице {x} - {len(images_links)} снимков')

        for i in range(len(images_links)):  # (len(images_links)):
            text_edit_link = make_text_edit_link(images_links[i].get('href'))
            driver.get(text_edit_link)
            time.sleep(1)
            try:
                keywords = driver.find_element(By.NAME, 'KeywordsRus').text
                good_keywords = ""
                driver.find_element(By.NAME, 'KeywordsRus').clear()
                if what_to_do == 1:
                    print(f"{red} all keywords deleted{end}")
                elif what_to_do == 2:
                    good_keywords = keywords_opimization(keywords)  # прогоняем ключевые слова через оптимизатор
                    print(f"{green} keywords optimisation {end}")
                elif what_to_do == 3:
                    print(f"{green}keyword {end}{red}{keyword}{end}{green} was removed{end}")
                    good_keywords = remove_mistake(keyword, keywords)
                elif what_to_do == 4:
                    print(f"{green}keywords added {end}{red}{keyword}{end}{green} to images{end}")
                    add_new_keywords(new_keywords, keywords)

                set_keywords_to_site(good_keywords)

                temp_set = set(good_keywords.split(', '))
                keywords_collection.update(temp_set)
                temp_set.clear()
                print(f'{i:40}')
                print(f"keywords for image\n{green}{good_keywords}{end}\n")
            except Exception as ex:
                driver.save_screenshot('problem.png')
                print(ex)
                continue

    return keywords_collection


def main():
    # коллекция для сбора ключевых слов
    keyword = chose_input()  # keyword for work
    what_to_do = select_action(keyword)  # 2
    new_keywords = display_your_choice(what_to_do, keyword)
    keyword_link, images_number = keywords_search(keyword)
    keywords_collection = get_images_links(images_number, keyword_link, keyword, what_to_do, new_keywords)

    driver.close()
    driver.quit()
    if what_to_do > 1:
        print(keywords_collection)
        write_keywords_in_txt_file(keywords_collection)
    else:
        print(f"{red} all keywords deleted{end}")


if __name__ == '__main__':
    driver = autorization()
    main()
