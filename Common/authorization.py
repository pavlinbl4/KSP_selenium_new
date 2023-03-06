from selenium import webdriver
from selenium.webdriver.common.by import By
from Common.crome_options import setting_chrome_options
from Common.credentials import get_credentials


def autorization():
    browser = webdriver.Chrome(options=setting_chrome_options())
    login, password, first_loggin = get_credentials()
    browser.get(first_loggin)
    login_input = browser.find_element(By.ID, "login")
    login_input.send_keys(login)
    password_input = browser.find_element(By.ID, "password")
    password_input.send_keys(password)
    browser.find_element(By.NAME, "loginbtn").click()
    return browser

if __name__ == '__main__':
    autorization()


