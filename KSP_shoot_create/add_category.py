from Common.authorization import autorization
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from KSP_shoot_create.checkbox_output import create_checkbox_dict


def open_shoot_creation_page(browser):
    browser.find_element(By.CSS_SELECTOR,
                         "body > table.logotbl > tbody > tr:nth-child(3)"
                         " > td > table > tbody > tr > td:nth-child(2) > a").click()
    browser.find_element(By.ID,
                         "nav_shoots_change").click()
    return browser


def select_category(category_number, browser):
    wait = WebDriverWait(browser, 10)
    browser.execute_script("OpenPopupWindow('ShootSubjectsAdmin.asp')")
    wait.until(EC.number_of_windows_to_be(2))
    browser.switch_to.window(browser.window_handles[1])
    category = Select(browser.find_element(By.ID, 'SubjectID'))
    category.select_by_value(category_number)
    browser.find_element(By.XPATH, '//*[@id="addrow"]').click()
    browser.find_element(By.XPATH, '//*[@id="DivSubmit"]/input[1]').click()


def add_category_to_shoot():
    category_number = create_checkbox_dict()
    browser = autorization()
    browser = open_shoot_creation_page(browser)
    select_category(category_number, browser)






if __name__ == '__main__':
    add_category_to_shoot()

