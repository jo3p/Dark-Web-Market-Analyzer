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

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

logging.info("Program launched.")

with create_webdriver() as driver:
    logging.info("Firefox browser launched.")
    try:
        driver.get("http://counteuiwleiigv3.onion/")
        logging.info("Successfully connected to a counterfeit store!")
    except WebDriverException as e:
        logging.exception("Unable to load page. See attached exception traceback.")
    time.sleep(15)
