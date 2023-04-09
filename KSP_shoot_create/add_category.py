
from Common.authorization import autorization
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select


def open_shoot_creation_page():
    browser.find_element(By.CSS_SELECTOR,
                         "body > table.logotbl > tbody > tr:nth-child(3)"
                         " > td > table > tbody > tr > td:nth-child(2) > a").click()
    browser.find_element(By.ID,
                         "nav_shoots_change").click()


def select_category(category_number):
    wait = WebDriverWait(browser, 10)
    browser.execute_script("OpenPopupWindow('ShootSubjectsAdmin.asp')")
    wait.until(EC.number_of_windows_to_be(2))
    browser.switch_to.window(browser.window_handles[1])
    category = Select(browser.find_element(By.ID, 'SubjectID'))
    category.select_by_value(category_number)
    browser.find_element(By.XPATH, '//*[@id="addrow"]').click()
    browser.find_element(By.XPATH, '//*[@id="DivSubmit"]/input[1]').click()


if __name__ == '__main__':
    browser = autorization()
    open_shoot_creation_page()
    select_category('4000000')


