from crawling.driver import WebDriver
from crawling.crawler import WebCrawler
import logging
from multiprocessing.pool import ThreadPool
from helpers import log
from helpers.redirect import job
import time


if __name__ == '__main__':
    begin = time.time()
    # Initialize logging
    log.init_logging()
    logging.info("Program launched.")
    # Create master webdriver
    n_partitions = int(input('Enter number of partitions: '))
    first_driver = WebDriver(n_partitions)
    partitions = first_driver.run()
    # Create crawler instances and execute in parallel
    crawler_list = [WebCrawler(file_number=i + 1, page_range=partitions[i]) for i in range(n_partitions)]
    with ThreadPool(n_partitions) as p:
        p.map(job, crawler_list)
    end = time.time()
    logging.info(f"Total execution time: {end-begin}")
