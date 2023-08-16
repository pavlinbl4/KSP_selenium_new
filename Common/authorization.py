from selenium import webdriver
from selenium.webdriver.common.by import By
from Common.crome_options import setting_chrome_options
from Common.credentials import get_credentials


def autorization():
    driver = webdriver.Chrome(options=setting_chrome_options())
    login, password, first_loggin = get_credentials()
    driver.get(first_loggin)
    login_input = driver.find_element(By.ID, "login")
    login_input.send_keys(login)
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(password)
    driver.find_element(By.NAME, "loginbtn").click()
    return driver


if __name__ == '__main__':
    autorization()
