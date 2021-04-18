from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import logging
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import os
import numpy as np
import time


class WebDriver:
    def __init__(self, n_partitions: int = 1):
        # Load parameter settings
        with open('crawling/firefox_parameters.json') as f:
            self.parameters = json.load(f)
        self.driver = None
        self.n_partitions = n_partitions  # set the amount of partitions, default = 1

    def run(self, master=True):
        if not master:
            # Make the system wait for n seconds, to prevent too many drivers initializing simultaneously
            time.sleep(np.random.randint(1, 10))
        # Initiate webdriver instance
        self.create_driver()
        logging.info("Firefox browser launched.")
        # Open the store's homepage
        try:
            self.driver.get("http://worldps45uh3rhedmx7g3jgjf3vw52wkvvcastfm46fzrpwoc7f33lid.onion/")
            logging.info("Connected to the store")
        except WebDriverException:
            self.exit(message='Exception: Unable to load page. See attached exception traceback.')  # quit
        # Fill in page entry captcha
        self.wait_for_captcha(by=By.NAME, value='username')
        # Login to marketplace
        self.login()
        if master:  # If the driver instance is the master, we determine the partitions and close the connection
            # Go to the drugs page
            self.browse_to_drugs()
            partitions = self.get_partitions()
            self.exit()
            return partitions

    def create_driver(self):
        firefox_profile = FirefoxProfile('/etc/tor')
        for preference, value in self.parameters.items():
            firefox_profile.set_preference(preference, value)
        self.driver = Firefox(firefox_profile=firefox_profile)

    def wait_for_captcha(self, by, value):
        # explicitly wait for login page to appear. manually fill page-entry CAPTCHA
        try:
            WebDriverWait(self.driver, 200).until(EC.presence_of_element_located((by, value)))
        except TimeoutException:
            self.exit(message='Error: Timeout when entering CAPTCHA.')

    def login(self):
        try:
            self.driver.get("http://worldps45uh3rhedmx7g3jgjf3vw52wkvvcastfm46fzrpwoc7f33lid.onion/login")
            self.driver.execute_script(
                "window.open('http://worldps45uh3rhedmx7g3jgjf3vw52wkvvcastfm46fzrpwoc7f33lid.onion/captcha.png', "
                "'captcha-tab');")
            username_element = self.driver.find_element_by_css_selector('[name="username"]')
            username_element.click()
            username_element.clear()
            username_element.send_keys(os.environ['username'])
            password_element = self.driver.find_element_by_css_selector('[name="password"]')
            password_element.click()
            password_element.clear()
            password_element.send_keys(os.environ['password'])
            login_time = Select(self.driver.find_element_by_css_selector('[name="session_time"]'))
            login_time.select_by_value('360')
        except NoSuchElementException:
            self.exit(message='Error: Could not navigate to login page. ')
        # explicitly wait for the user to enter CAPTCHA after entering credentials, then move to homepage
        self.wait_for_captcha(by=By.ID, value='information')

    def browse_to_drugs(self):
        # checking main categories on marketplace
        categories = {}
        category_list = self.driver.find_elements_by_css_selector('[href*="/category/"]')
        for category in category_list:
            category_list_split = category.text.split('\n')
            name = ''.join(filter(str.isalpha, category_list_split[0]))
            categories[name] = category.get_attribute('href')
        # navigate to drugs section
        self.driver.get(categories['Drugs'])

    def get_partitions(self):
        n_pages = int(self.driver.find_element_by_class_name('lastP').
                      find_element_by_css_selector("a").
                      get_attribute("href").
                      split("=")[-1])
        step = n_pages / self.n_partitions
        return [(round(step * i) + 1, round(step * (i + 1))) for i in range(self.n_partitions)]

    def exit(self, message="Firefox terminated"):
        self.driver.quit()
        logging.info(message)
