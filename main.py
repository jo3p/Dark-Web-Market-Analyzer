import logging
import os
from helpers import init_logging, WebDriver, WebCrawler, crawl
from multiprocessing.pool import ThreadPool

###
# Initialize logging
init_logging()
logging.info("Program launched.")

# Initialize webdriver class
first_driver = WebDriver()
first_driver.run()

# login and return to homepage
first_driver.login()

# Browse to drugs page
first_driver.browse_to_drugs()

# Create partitions
n_partitions = 4
partitions = first_driver.get_partitions(n_partitions=n_partitions)
first_driver.exit()

# Create n driver objects
driver_list = [WebDriver() for i in range(n_partitions)]
crawler_list = [WebCrawler(driver=driver_list[i].driver, file_number=i+1, page_range=partitions[i])
                for i in range(n_partitions)]

for driver in driver_list:
    driver.run()
    driver.login()

if not os.path.exists('data'):
    os.makedirs('data')

with ThreadPool(n_partitions) as p:
    p.map(crawl, crawler_list)
