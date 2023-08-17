"""
Work with the image description page that is
available when you press the button with the hammer and wrench icon.
"""

from selenium.webdriver.common.by import By

from Common.authorization import autorization
from Common.selenium_tools import go_my_images, end_selenium


def grab_image_info_page(driver, html):
    driver.get(html)
    keywords = driver.find_element(By.NAME, 'KeywordsRus').text  # copy keywords from field image info page
    image_id = driver.find_element(By.CSS_SELECTOR, '#photoPreview > span:nth-child(2)').text
    caption = driver.find_element(By.XPATH, '//*[@id="DescriptionRus"]').text
    return image_id, caption, keywords


if __name__ == '__main__':
    t_driver = autorization()
    print(grab_image_info_page(t_driver,
                               html='https://image.kommersant.ru/photo/archive/adm/AddPhotoStep3.asp?ID=3807024&CloseForm=1'))
    end_selenium(t_driver)
