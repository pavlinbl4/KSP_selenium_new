from selenium.webdriver.common.by import By
from shoot_history.make_page_link import make_history_link


def check_shoot_id(shoot_id, browser):
    id_input = browser.find_element(By.ID, "code")
    id_input.clear()
    id_input.send_keys(shoot_id)
    browser.find_element(By.CSS_SELECTOR, '#searchbtn').click()


def open_page(page_link, browser):
    browser.get(page_link)


def work_to_history(browser):
    browser.find_element(By.ID, 'ctl00_MainContent_ShootInfoForm_FullShootNumber').click()
    browser.find_element(By.CLASS_NAME, 'history-header').click()
    first_link = browser.current_url
    full_link = make_history_link(first_link)  # получаю ссылку на страницу с подробной историей
    browser.get(full_link)  # открывается новая вкладка, нужно перейти на нее
    browser.switch_to.window(browser.window_handles[0])
    return browser.page_source


def end_selenium(browser):
    browser.close()
    browser.quit()


# report_web_link = 'https://image.kommersant.ru/photo/archive/pubhistory.asp?ID='
