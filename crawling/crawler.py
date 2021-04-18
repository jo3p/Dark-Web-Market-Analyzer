from crawling.driver import WebDriver
import logging
from datetime import date
from helpers.cd import create_directory


class WebCrawler(WebDriver):
    def __init__(self, file_number, page_range):
        super().__init__()
        self.thread_number = file_number
        self.page_range = page_range
        self.listings_directory = self.sellers_directory = None
        self.sellers = []

    def initialize_directories(self):
        # Create data folder if not present
        create_directory(path='data')
        # Create subdirectory with date
        date_directory = f"data/{date.today()}"
        create_directory(path=date_directory)
        # Create subdirectories for listings and sellers
        self.listings_directory = f"data/{date.today()}/listings"
        create_directory(path=self.listings_directory)
        self.sellers_directory = f"data/{date.today()}/sellers"
        create_directory(path=self.sellers_directory)

    def crawl(self):
        # Create a webdriver instance with WebDriver class and Login to the marketplace
        self.run(master=False)  # load home page, solve captcha, and login.
        logging.info(f"Start Crawling - {self.thread_number}")
        # Create the directory structure
        self.initialize_directories()
        # For all pages in the page range, crawl the listings and sellers
        for page_no in range(self.page_range[0], self.page_range[1] + 1):
            # Navigate to the listings overview page
            url = f"http://worldps45uh3rhedmx7g3jgjf3vw52wkvvcastfm46fzrpwoc7f33lid.onion/category/1?page={page_no}"
            self.driver.get(url)
            # Extract listing URL's from overview page
            listing_divs = self.driver.find_elements_by_class_name("col-1search")
            listing_urls = [i.find_element_by_css_selector("a").get_attribute("href") for i in listing_divs]
            logging.debug(f"Scraped page {page_no} from thread {self.thread_number}")
            # Visit and save urls
            for url in listing_urls:
                self.save_listing(url)
                self.save_seller()
        self.exit()

    def save_listing(self, url):
        # Save page source to disk in separate folder
        self.driver.get(url)
        file_name = f"{self.listings_directory}/{url.replace('/', '-')}"
        with open(file_name, 'a') as file:
            file.write(self.driver.page_source)

    def save_seller(self):
        # Extract listing description
        ld = self.driver.find_element_by_css_selector(".listDes > p:nth-child(2) > b:nth-child(1) > a:nth-child(1)")
        # Extract seller page url and save to disk
        seller_url = ld.get_attribute("href")
        # Check if the seller is already visited
        if seller_url not in self.sellers:
            self.driver.get(seller_url)
            file_name = f"{self.sellers_directory}/{seller_url.replace('/', '-')}"
            with open(file_name, 'a') as file:
                file.write("%s\n" % seller_url)
            self.sellers.append(seller_url)
