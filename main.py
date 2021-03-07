import time
import logging
import pandas as pd

from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.keys import Keys

from driver import create_webdriver

logging.basicConfig(
    filename='logfile.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%d-%m-%Y %H:%M:%S')


with create_webdriver() as driver:
    driver.get("https://check.torproject.org/")
    time.sleep(30)
