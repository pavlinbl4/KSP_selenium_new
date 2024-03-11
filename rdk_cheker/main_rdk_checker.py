import re
import pickle

from selenium import webdriver
from datetime import date

import os
from dotenv import load_dotenv

from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service

from rdk_cheker.check_article_status import check_article_status
from rdk_cheker.delete_old_pickle import delete_old_pickle
from rdk_cheker.send_message_to_telegram import send_telegram_message

service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service)


def find_date(str_with_date='№24 Пн, 05.02.24'):
    re_pattern = r'\d{2}\.\d{2}\.\d{2}'
    return re.findall(re_pattern, str_with_date)[0]


def find_article_status(article_status='GetImage.axd?kind=WF&key=E&site=RDK2SPB'):
    pattern = r'(?<=key=).*(?==RDK2SPB)'
    return re.findall(pattern, article_status)[0]


def get_spans():
    load_dotenv()
    rdk_logging = os.environ.get('rdk_logging')
    driver.get(rdk_logging)
    driver.get('https://rdk.spb.kommersant.ru:9443/rdk2/?p=RDK2SPB,NODE:2353975')
    all_spans = driver.find_elements('xpath', '//span[@id="phList"]/a')
    return all_spans


def get_today_link(all_spans):
    today = date.today().strftime("%d.%m.%y")
    # today_link = None
    for span in all_spans:
        if find_date(span.text) == today:
            today_link = span.get_attribute('href')
            return today_link


def get_article_status():
    today_filename = date.today().strftime("%d_%m_%y")
    delete_old_pickle(today_filename)
    all_spans = get_spans()
    articles_dict = {}
    if os.path.exists(f'{today_filename}.pickle'):
        with open(f'{today_filename}.pickle', 'rb') as data_file:
            articles_dict = pickle.load(data_file)
    # print(articles_dict)
    today_link = get_today_link(all_spans)
    driver.get(today_link)  # '//tr[@class="mapLO"][2]/td[6]/img'
    work_map = driver.find_elements('xpath', '//tr[@class="mapLO"]')

    for x in range(1, len(work_map)):
        all_trs = work_map[x].find_elements('xpath', 'td')
        article_name = all_trs[0].text
        article_status = find_article_status(all_trs[5].find_element('xpath', 'img').get_attribute('src'))
        if len(article_name) > 0 and article_name not in articles_dict:
            print(article_name)
            print(article_status)
            send_telegram_message(f'{article_name} - {article_status}')
            articles_dict[article_name] = article_status
            with open(f'{today_filename}.pickle', 'wb') as f:
                pickle.dump(articles_dict, f)
        else:
            check_article_status(article_name, article_status, today_filename)

    driver.close()
    driver.quit()


if __name__ == '__main__':
    get_article_status()

