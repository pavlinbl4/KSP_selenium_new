''' add watching count to article'''

import time
from selenium import webdriver
from selenium.common import WebDriverException

from Common.crome_options import setting_chrome_options
from Common.selenium_tools import end_selenium
from tqdm import trange
import multiprocessing
import random
from icecream import ic


def read_proxy():
    with open('proxy_list.txt', 'r') as text_file:
        return text_file.readlines()


def ring_page(i, article_url):

    chrome_options = setting_chrome_options()

    # chrome_options.add_argument("--headless")  # фоновый режим

    # chrome_options.add_argument('--proxy-server=%s' % proxy.strip())

    # Initialize Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    for x in trange(30):
        # Sleep random amount of time
        time.sleep(random.randint(1, 3))

        # Load page
        driver.get(article_url)

    # Cleanup
    end_selenium(driver)

    # except WebDriverException as e:
    #
    #     if e.msg == "ERR_PROXY_CONNECTION_FAILED":
    #         print("Failed to connect through the proxy")

    # else:
    #     print(f"Connected successfully through proxy - {proxy.strip()}")


def main(article_url):
    processes = []
    for i in range(6):
        p = multiprocessing.Process(target=ring_page, args=(i, article_url))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


if __name__ == '__main__':
    main('https://www.kommersant.ru/doc/6397031')
