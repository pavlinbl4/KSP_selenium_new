"""
Work with the image description page that is
available when you press the button with the hammer and wrench icon.
"""

from Common.authorization import autorization
from selenium.common.exceptions import NoSuchElementException
from Common.regex_tools import replace_to_comma
from Common.save_info_in_csv import write_kp_files_keywords
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def set_keywords_to_site(good_keywords, driver):
    # main_window = driver.current_window_handle
    # try:
    driver.find_element(By.NAME, 'KeywordsRus').clear()
    driver.find_element(By.NAME, 'KeywordsRus').send_keys(good_keywords)
    driver.find_element(By.NAME, 'Add').click()

        # wait = WebDriverWait(driver, 1)
        # alert = wait.until(EC.alert_is_present())
        #
        # if alert:
        #     alert.accept()


    # except TimeoutException:
    #     print('no TimeoutException')

    # driver.switch_to.window(main_window)
    # driver.find_element(By.ID, 'DescriptionRus').click()
    # driver.find_element(By.ID, 'DescriptionRus').send_keys('требуется описание')
    # driver.find_element(By.NAME, 'Add').click()


def grab_image_info_page(driver, info_page_url):
    try:
        driver.get(info_page_url)
        keywords = driver.find_element(By.ID, 'KeywordsRus').get_attribute('value')
        image_id = driver.find_element(By.ID, 'photoPreview').find_element(By.TAG_NAME, 'span').text
        caption = driver.find_element(By.ID, 'DescriptionRus').get_attribute('value')

    except NoSuchElementException:
        print("One of the elements was not found on the page")
        return None, None, None

    return image_id, caption, keywords


def image_info_optimization(driver, text_edit_link):
    image_id, caption, keywords = grab_image_info_page(driver, text_edit_link)  # grab info

    # if keywords not empty - optimise it
    if keywords != '' and keywords is not None:
        write_kp_files_keywords(image_id, caption, keywords)  # save data in csv file

        optimized_keywords = replace_to_comma(keywords)  # replace ; with comma
        print(optimized_keywords)

        set_keywords_to_site(optimized_keywords, driver)  # write optimized keywords to site


if __name__ == '__main__':
    t_driver = autorization()
    # print(grab_image_info_page(t_driver,
    #                            info_page_url='https://image.kommersant.ru/photo/archive/adm/AddPhotoStep3.asp?ID=3807024&CloseForm=1'))

    image_info_optimization(t_driver,
                            'https://image.kommersant.ru/photo/archive/adm/AddPhotoStep3.asp?ID=2582832&CloseForm=1')
