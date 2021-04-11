import os
from crawling.driver import WebDriver
from crawling.crawler import WebCrawler
import logging
from multiprocessing.pool import ThreadPool
from helpers import log


#
# with ThreadPool(n_partitions) as p:
#     p.map(crawl, crawler_list)


if __name__ == '__main__':
    # Initialize logging
    log.init_logging()
    logging.info("Program launched.")
    # Create master webdriver
    n_partitions = 2
    first_driver = WebDriver(n_partitions)
    partitions = first_driver.run()
    # Create crawler instances
    crawler_list = [WebCrawler(file_number=i + 1, page_range=partitions[i]) for i in range(n_partitions)]
    # Log in crawlers
    for crawler in crawler_list:
        crawler.start()  # Starts a parallel process
    # # # Parallelize and execute crawlers
    # for crawler in crawler_list:
    #     crawler.start()

# if __name__ == '__main__':
#     x = WebCrawler(file_number=1, page_range=(1, 20))
#     x.crawl()
