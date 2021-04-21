from crawling.driver import WebDriver
from crawling.crawler import WebCrawler
from scraping.scraper import DocumentParser
import logging
from multiprocessing.pool import ThreadPool
from helpers.log import init_logging
from helpers.redirect import job
import time
import datetime as dt
import pandas as pd

if __name__ == '__main__':
    begin = time.time()
    # Initialize logging
    logging = init_logging()
    # Create master webdriver
    n_partitions = int(input('Enter number of parallel threads: '))
    first_driver = WebDriver(n_partitions)
    partitions = first_driver.run()
    # Create crawler instances and execute in parallel
    crawler_list = [WebCrawler(file_number=i + 1, page_range=partitions[i]) for i in range(n_partitions)]
    with ThreadPool(n_partitions) as p:
        p.map(job, crawler_list)
    end = time.time()
    logging.info(f"Total execution time: {end - begin}")

    # Scrape crawled data
    parser = DocumentParser(dt.date.today())
    parser.scrape()
    parser.save_as_parquet()
    test_df = pd.read_parquet(parser.listings_save_location)
