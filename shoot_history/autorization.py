from selenium.webdriver.common.by import By
from shoot_history.make_page_link import make_history_link


def check_shoot_id(shoot_id, driver):
    id_input = driver.find_element(By.ID, "code")
    id_input.clear()
    id_input.send_keys(shoot_id)
    driver.find_element(By.CSS_SELECTOR, '#searchbtn').click()


def open_page(page_link, driver):
    driver.get(page_link)


def work_to_history(driver):
    driver.find_element(By.ID, 'ctl00_MainContent_ShootInfoForm_FullShootNumber').click()
    driver.find_element(By.CLASS_NAME, 'history-header').click()
    first_link = driver.current_url
    full_link = make_history_link(first_link)  # получаю ссылку на страницу с подробной историей
    driver.get(full_link)  # открывается новая вкладка, нужно перейти на нее
    driver.switch_to.window(driver.window_handles[0])
    return driver.page_source






