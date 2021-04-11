import os
from crawling.driver import WebDriver
from crawling.crawler import WebCrawler
import logging
from multiprocessing.pool import ThreadPool
from helpers import log

###
# Initialize logging
log.init_logging()
logging.info("Program launched.")

# Initialize webdriver class
first_driver = WebDriver(n_partitions=1)
partitions = first_driver.run(master=True)

# # login and return to homepage
# first_driver.login()
#
# # Browse to drugs page
# first_driver.browse_to_drugs()
#
# # Create partitions
# n_partitions = 4
# partitions = first_driver.get_partitions(n_partitions=n_partitions)
# first_driver.exit()

# Create n driver objects
# driver_list = [WebDriver() for i in range(n_partitions)]
# crawler_list = [WebCrawler(driver=driver_list[i].driver, file_number=i+1, page_range=partitions[i])
#                 for i in range(n_partitions)]
#
# for driver in driver_list:
#     driver.run()
#     driver.login()
#
# if not os.path.exists('data'):
#     os.makedirs('data')
#
# with ThreadPool(n_partitions) as p:
#     p.map(crawl, crawler_list)


if __name__ == '__main__':
    pass


