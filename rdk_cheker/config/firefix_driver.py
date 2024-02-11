import os
from dotenv import load_dotenv
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from datetime import date
import re


def find_date(str_with_date='№24 Пн, 05.02.24'):
    re_pattern = r'\d{2}\.\d{2}\.\d{2}'
    return re.findall(re_pattern, str_with_date)[0]


class FireFoxDriver:

    def __init__(self):
        load_dotenv()
        self.rdk_logging = os.environ.get('rdk_logging')
        self.service = Service(GeckoDriverManager().install())
        self.today = date.today().strftime("%d.%m.%y")
        self.driver = None
        self.all_spans = None
        self.today_link = None

    def setup_driver(self):
        self.driver = webdriver.Firefox(service=self.service)

    def get_driver(self):
        return self.driver

    def perform_authorization(self):
        self.setup_driver()
        self.driver.get(self.rdk_logging)

    def authorize(self):
        self.perform_authorization()

    def get_all_notes(self):
        self.authorize()
        self.driver.get('https://rdk.spb.kommersant.ru:9443/rdk2/?p=RDK2SPB,NODE:2353975')
        self.all_spans = self.driver.find_elements('xpath', '//span[@id="phList"]/a')
        return self.all_spans

    def get_today_note(self):
        self.get_all_notes()
        for span in self.all_spans:
            if find_date(span.text) == self.today:
                self.today_link = span.get_attribute('href')
                return self.today_link

    def get_today_articles(self):
        self.today_link = self.get_today_note()
        self.driver.get(self.today_link)  # '//tr[@class="mapLO"][2]/td[6]/img'
        work_map = self.driver.find_elements('xpath', '//tr[@class="mapLO"]')
        for x in range(1, len(work_map)):
            all_trs = work_map[x].find_elements('xpath', 'td')
            print(all_trs[0].text)
            print(all_trs[5].find_element('xpath', 'img').get_attribute('src'))


if __name__ == '__main__':
    first_enter = FireFoxDriver().get_today_articles()
