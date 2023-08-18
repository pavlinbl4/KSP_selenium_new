"""
Work with the image description page that is
available when you press the button with the hammer and wrench icon.
"""

from Common.authorization import autorization
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver.common.by import By


def grab_image_info_page(driver, info_page_url):
    try:
        driver.get(info_page_url)
        keywords = driver.find_element(By.ID, 'KeywordsRus').get_attribute('value')
        image_id = driver.find_element(By.ID, 'photoPreview').find_element(By.TAG_NAME, 'span').text
        caption = driver.find_element(By.ID, 'DescriptionRus').get_attribute('value')

    except UnexpectedAlertPresentException:
        alert = driver.switch_to.alert
        alert.accept()
        print("Alert window")

    except NoSuchElementException:
        print("One of the elements was not found on the page")
        return None, None, None

    return image_id, caption, keywords


if __name__ == '__main__':
    t_driver = autorization()
    print(grab_image_info_page(t_driver,
                               info_page_url='https://image.kommersant.ru/photo/archive/adm/AddPhotoStep3.asp?ID=3807024&CloseForm=1'))
