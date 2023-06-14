from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def find_images_by_id(shoot_id, browser):  # авторизация гна главной странице
    browser.find_element(By.CSS_SELECTOR, '#code').clear()
    browser.find_element(By.CSS_SELECTOR, '#code').send_keys(shoot_id)
    browser.find_element(By.CSS_SELECTOR, '#lib0').click()
    select = Select(browser.find_element(By.NAME, 'ps'))
    select.select_by_value('100')
    browser.find_element(By.CSS_SELECTOR, '#searchbtn').click()
    link = browser.current_url
    return link
