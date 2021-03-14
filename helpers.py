import logging

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def login(driver, username, password):
    try:  # explicitly wait for login page to appear. manually fill page-entry CAPTCHA
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.NAME, 'username')))
    except TimeoutException:
        driver.quit()
        logging.error('Timeout when entering CAPTCHA.')
    finally:
        try:
            username_element = driver.find_element_by_css_selector('[name="username"]')
            username_element.click()
            username_element.clear()
            username_element.send_keys(username)
            password_element = driver.find_element_by_css_selector('[name="password"]')
            password_element.click()
            password_element.clear()
            password_element.send_keys(password)
            login_time = Select(driver.find_element_by_css_selector('[name="session_time"]'))
            login_time.select_by_value('360')
        except NoSuchElementException:
            logging.error('Could not navigate to login page.')

    try:  # explicitly wait for the user to enter CAPTCHA after entering credentials, then move to homepage
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, 'information')))
    except TimeoutException:
        driver.quit()
        logging.error('Timeout when entering CAPTCHA.')
    finally:
        pass
