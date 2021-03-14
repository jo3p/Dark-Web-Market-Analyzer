import time
import logging
from selenium.common.exceptions import WebDriverException

from driver import create_webdriver
from helpers import login

USERNAME = 'sdfu3422532'
PASSWORD = 'yu@53%sgsdfg67!te'

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

# launch webdriver
with create_webdriver() as driver:
    logging.info("Firefox browser launched.")
    try:
        driver.get("http://worldps45uh3rhedmx7g3jgjf3vw52wkvvcastfm46fzrpwoc7f33lid.onion/login")
        logging.info("Successfully connected to the store!")
    except WebDriverException as e:
        logging.exception("Unable to load page. See attached exception traceback.")

    # login and return to homepage
    login(driver, USERNAME, PASSWORD)

    # checking main categories on marketplace
    categories = {}
    category_list = driver.find_elements_by_css_selector('[href*="/category/"]')
    for category in category_list:
        category_list_split = category.text.split('\n')
        name = ''.join(filter(str.isalpha, category_list_split[0]))
        amount = int(category_list_split[1])
        categories[name] = category.get_attribute('href')

    # navigate to drugs section
    driver.get(categories['Drugs'])

    # collect all drug categories in drugs section
    drug_categories = {}  # dict containing all drug-categories (keys) and links (values)
    for drug_category in driver.find_element_by_class_name('submenu').text.split('⩾')[1:]:
        drug_name, drug_amount = drug_category.split('\n')[0].strip(), int(drug_category.split('\n')[1])
        drug_categories[drug_name] = int(drug_amount)
    drug_names = list(drug_categories.keys())  # list containing all drug names as stripped strings

    time.sleep(100)
