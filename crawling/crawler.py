from crawling.driver import WebDriver
import logging
from datetime import date
from helpers.cd import create_directory


class WebCrawler(WebDriver):
    def __init__(self, file_number, page_range):
        # super(WebCrawler, self).__init__()  # Inherit all methods and properties
        # multiprocessing.Process.__init__(self)
        super().__init__()
        self.thread_number = file_number
        self.file_name = f"listing_URLs_{file_number}.txt"
        self.page_range = page_range
        print(self.parameters)

    def crawl(self):
        # Create a webdriver instance with WebDriver class and Login to the marketplace
        self.run(master=False)  # load home page, solve captcha, and login.
        # create data directory
        create_directory(path='data')
        logging.info(f"Start Crawling - {self.thread_number}")
        for page_no in range(self.page_range[0], self.page_range[1] + 1):
            # Navigate to the listings overview page
            url = f"http://worldps45uh3rhedmx7g3jgjf3vw52wkvvcastfm46fzrpwoc7f33lid.onion/category/1?page={page_no}"
            self.driver.get(url)
            # Extract listing URL's from overview page
            listing_divs = self.driver.find_elements_by_class_name("col-1search")
            listing_urls = [i.find_element_by_css_selector("a").get_attribute("href") for i in listing_divs]
            logging.debug(f"Scraped page {page_no} from thread {self.thread_number}")
            # Append listing URL to file
            with open(self.file_name, 'a') as file:
                for url in listing_urls:
                    file.write("%s\n" % url)
            # Save page source to disk in separate folder
            for url in listing_urls:
                self.driver.get(url)
                directory = f"data/{date.today()}"
                create_directory(path=directory)
                with open(directory + '/' + url.replace("/", "-"), 'a') as file:
                    file.write(self.driver.page_source)
        self.exit()
