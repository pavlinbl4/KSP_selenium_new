"""script download my published shoots to selected folder
pip install beautifulsoup4
pip install selenium
pip install lxml
"""
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from Common.download_to_selected_folder import enable_download
from Common.regex_tools import make_preview_photo_link
from Common.selenium_tools import find_all_images_on_site_by_shoot_id_or_keyword, page_source_from_selenium
from Common.soup_tools import get_image_links
from kp_selenium_tools.authorization import AuthorizationHandler
from loguru import logger

from kp_selenium_tools.remove_image import delete_image_in_kp_photo_archive

# logger.disable('__main__')
logger.add("output.log", format="{time} {level} {message}", level="ERROR")
logger.add("output.log", format="{time} {level} {message}", level="INFO")


def make_shoot_edit_link(link):
    shoot_edit_link = f'https://image.kommersant.ru/photo{link[2:]}'
    return shoot_edit_link


def main_cycle(number_of_shots, link, driver):
    deleted_count = 0
    count = 0
    range_number = number_of_shots // 100 + 2  # количество страниц выданных поиском
    for x in range(1, range_number):  # цикл по страницам съемки
        page_link = f'{link}2&pg={x}'  # ссылка на страницу с номером
        html = page_source_from_selenium(page_link, keyword=[], driver=driver)  # получаю html открытой страницы
        images_links = get_image_links(html)  # получаю список ссылок редактирование изображения
        logger.info(f'на странице {x} - {len(images_links)} снимков')
        for i in range(len(images_links)):  # (len(images_links)):
            preview_photo_window_link, image_id, inner_id = make_preview_photo_link(images_links[i].get('href'))
            shoot_edit_link = make_shoot_edit_link(images_links[i].get('href'))

            driver.get(shoot_edit_link)

            # click to download image
            try:
                driver.find_element(By.CSS_SELECTOR,
                                    f"div.hi-subpanel:nth-child(3) > a:nth-child(4)").click()
                logger.info(f'downloading image {image_id}')

                # function to delete images
                try:
                    driver.get(preview_photo_window_link)
                    count, deleted_count = delete_image_in_kp_photo_archive(driver, count, image_id, deleted_count)
                except NoSuchElementException:
                    logger.info(f"Couldn't delite image {image_id}")
            except NoSuchElementException:
                logger.info(f"Couldn't download  image {image_id}")
    logger.info(f'deleted {deleted_count} images')


def main_kp_downloader(shoot_id, download_dir, keyword):
    # authorization on site and enable selected download folder
    driver = AuthorizationHandler().authorize()
    enable_download(driver, download_dir)

    link, number_of_shots = find_all_images_on_site_by_shoot_id_or_keyword(driver, shoot_id, keyword=keyword,
                                                                           only_kr=True)
    logger.info(number_of_shots)

    main_cycle(number_of_shots, link, driver)
    time.sleep(5)

    driver.close()
    driver.quit()
    logger.info(f'Work completed for shoot {shoot_id}', f'{number_of_shots} files downloaded to {download_dir}')


if __name__ == '__main__':
    shoot_id_ = ''

    download_dir_ = f'/Volumes/big4photo-4/selenium_downloads/keyword_слон'
    main_kp_downloader(shoot_id_, download_dir_, 'слон')
