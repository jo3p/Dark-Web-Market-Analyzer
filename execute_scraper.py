from time import time
from scraping.scraper import DocumentParser
from helpers.log import init_logging
# import logging

if __name__ == '__main__':
    logging = init_logging()
    start_time = time()
    parser = DocumentParser(verbose=True)
    parser.scrape(scrape_listings=True, scrape_sellers=False)
    parser.save_as_parquet()
    parser.save_to_sql_db()
    logging.info(f'Finished parsing! Total execution time: {time() - start_time}s')
