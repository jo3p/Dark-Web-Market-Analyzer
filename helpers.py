from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import logging
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def init_logging():
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


# class WebDriver:
#     """
#     Extends the chromedriver class to be used as context manager.
#     """
#
#     def __init__(self, driver):
#         self.driver = driver
#
#     def __enter__(self):
#         return self.driver
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.driver.quit()
#         logging.info('Firefox terminated.')

class WebDriver:
    def __init__(self):
        firefox_profile = FirefoxProfile('/etc/tor')
        # set some privacy settings
        firefox_profile.set_preference("places.history.enabled", False)
        firefox_profile.set_preference("privacy.clearOnShutdown.offlineApps", True)
        firefox_profile.set_preference("privacy.clearOnShutdown.passwords", True)
        firefox_profile.set_preference("privacy.clearOnShutdown.siteSettings", True)
        firefox_profile.set_preference("privacy.sanitize.sanitizeOnShutdown", True)
        firefox_profile.set_preference("signon.rememberSignons", False)
        firefox_profile.set_preference("network.cookie.lifetimePolicy", 2)
        firefox_profile.set_preference("network.dns.disablePrefetch", True)
        firefox_profile.set_preference("network.http.sendRefererHeader", 0)
        # set socks proxy
        firefox_profile.set_preference("network.proxy.type", 1)
        firefox_profile.set_preference("network.proxy.socks_version", 5)
        firefox_profile.set_preference("network.proxy.socks", '127.0.0.1')
        firefox_profile.set_preference("network.proxy.socks_port", 9050)
        firefox_profile.set_preference("network.proxy.socks_remote_dns", True)
        # if you're really hardcore about your security
        # js can be used to reveal your true i.p.
        firefox_profile.set_preference("javascript.enabled", False)
        # get a huge speed increase by not downloading images
        firefox_profile.set_preference("permissions.default.image", 2)
        self.driver = Firefox(firefox_profile=firefox_profile)

    def login(self):
        username = 'sdfu3422532'
        password = 'yu@53%sgsdfg67!te'
        try:  # explicitly wait for login page to appear. manually fill page-entry CAPTCHA
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.NAME, 'username')))
        except TimeoutException:
            self.driver.quit()
            logging.error('Timeout when entering CAPTCHA.')
        finally:
            try:
                self.driver.execute_script(
                    "window.open('http://worldps45uh3rhedmx7g3jgjf3vw52wkvvcastfm46fzrpwoc7f33lid.onion/captcha.png', "
                    "'captcha-tab');")
                username_element = self.driver.find_element_by_css_selector('[name="username"]')
                username_element.click()
                username_element.clear()
                username_element.send_keys(username)
                password_element = self.driver.find_element_by_css_selector('[name="password"]')
                password_element.click()
                password_element.clear()
                password_element.send_keys(password)
                login_time = Select(self.driver.find_element_by_css_selector('[name="session_time"]'))
                login_time.select_by_value('360')
            except NoSuchElementException:
                logging.error('Could not navigate to login page.')
        try:  # explicitly wait for the user to enter CAPTCHA after entering credentials, then move to homepage
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.ID, 'information')))
        except TimeoutException:
            self.driver.quit()
            logging.error('Timeout when entering CAPTCHA.')
        finally:
            pass

    def run(self):
        logging.info("Firefox browser launched.")
        try:
            self.driver.get("http://worldps45uh3rhedmx7g3jgjf3vw52wkvvcastfm46fzrpwoc7f33lid.onion/")
            logging.info("Successfully connected to the store!")
        except WebDriverException as e:
            logging.exception("Unable to load page. See attached exception traceback.")
        # login and return to homepage
        self.login()

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

    def get_partitions(self, n_partitions):
        n_pages = int(self.driver.find_element_by_class_name('lastP').
                      find_element_by_css_selector("a").
                      get_attribute("href").
                      split("=")[-1])
        step = n_pages / n_partitions
        return [(round(step * i) + 1, round(step * (i + 1))) for i in range(n_partitions)]

    def exit(self):
        self.driver.quit()
        logging.info('Firefox terminated.')


class WebCrawler:
    def __init__(self, driver, file_number, page_range):
        self.driver = driver
        self.thread_number = file_number
        self.file_name = f"listing_URLs_{file_number}.txt"
        self.page_range = page_range


def crawl(webdriver_obj):
    logging.info(f"Start Crawling - {webdriver_obj.thread_number}")
    for page_no in range(webdriver_obj.page_range[0], webdriver_obj.page_range[1] + 1):
        webdriver_obj.driver.get(
            f"http://worldps45uh3rhedmx7g3jgjf3vw52wkvvcastfm46fzrpwoc7f33lid.onion/category/1?page={page_no}")
        # Extract listing URL's from source page
        listing_divs = webdriver_obj.driver.find_elements_by_class_name("col-1search")
        listing_urls = [i.find_element_by_css_selector("a").get_attribute("href") for i in listing_divs]
        logging.debug(f"Scraped page {page_no} from thread {webdriver_obj.thread_number}")
        with open(webdriver_obj.file_name, 'a') as file:
            for url in listing_urls:
                file.write("%s\n" % url)

        # store the listings on the page to disk.
        for url in listing_urls:
            webdriver_obj.driver.get(url)
            with open("data/" + url.replace("/", "-"), 'a') as file:
                file.write(webdriver_obj.driver.page_source)
    webdriver_obj.exit()
