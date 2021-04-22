from bs4 import BeautifulSoup
from pathlib import Path
import os
import datetime as dt
import pandas as pd
from time import time
from helpers.database import DbConnection
from helpers.log import init_logging
import logging


class DocumentParser:
    """
    Class that parses (scrapes) the crawled webpages in the "listings" and "sellers" directories
    """
    def __init__(self, verbose=False):
        self.verbose = verbose
        # Define the folder structure
        self.work_dir = Path(os.getcwd())
        self.scrape_date = self.process_input_date(
            input('Give in scrape date in the following format: dd-mm-yyyy. Press enter for today.'))
        self.scrape_dir = self.work_dir / 'data' / str(self.scrape_date)
        self.listings_dir = self.scrape_dir / 'listings'
        self.sellers_dir = self.scrape_dir / 'sellers'
        self.listings_save_location = self.scrape_dir / 'scraped_listings.gzip'
        self.sellers_save_location = self.scrape_dir / 'scraped_sellers.gzip'

        # Define an attribute for the final result
        self.listings = pd.DataFrame()
        self.sellers = pd.DataFrame()

    def scrape(self, scrape_listings=True, scrape_sellers=False):
        """
        Method that initiates the parsing of listings and sellers and appends the results to the corresponding dataframe
        """
        logging.info('Started parsing!')
        if scrape_listings:
            # scrape listings
            no_of_listings = len(os.listdir(self.listings_dir))
            for i, file in enumerate(os.listdir(self.listings_dir)):
                if self.verbose:
                    logging.info(f'Parsing listing {i}/{no_of_listings}: {file.replace("-", "/")}')
                listing = self.parse_listing(self.listings_dir / file)

                # append listing (pd.Series) to listings (pd.DataFrame)
                if len(self.listings) == 0:
                    self.listings = pd.concat([self.listings, listing.to_frame().T])
                elif listing['Title'].lower() not in self.listings['Title'].str.lower().values:
                    self.listings = pd.concat([self.listings, listing.to_frame().T])
        # scrape sellers
        if scrape_sellers:
            no_of_sellers = len(os.listdir(self.sellers_dir))
            for i, file in enumerate(os.listdir(self.sellers_dir)):
                if self.verbose:
                    logging.info(f'Parsing seller {i}/{no_of_sellers}: {file.replace("-", "/")}')
                seller = self.parse_seller(self.sellers_dir / file)

                # append listing (pd.Series) to listings (pd.DataFrame)
                if len(self.sellers) == 0:
                    self.sellers = pd.concat([self.sellers, seller.to_frame().T])
                elif seller['Seller Name'].lower() not in self.sellers['Seller Name'].str.lower().values:
                    self.sellers = pd.concat([self.sellers, seller.to_frame().T])

    def parse_listing(self, file: Path) -> pd.Series:
        """
        Method that scrapes the given listing and returns a pandas Series with the scraped results
        :param file: Path of the html file to be parsed
        :return: pd.Series with the scraped results
        """

        # Create empty Series to store results in
        result = pd.Series(dtype='object')

        # Load html file
        listing = self.open_html(file)

        # Select most important info element on page
        list_desc = listing.find(class_='listDes')

        # Get general stats
        result['Seller Name'] = list_desc.find('a').text.strip()
        result['Scrape Date'] = self.scrape_date
        result['Title'] = list_desc.find('h2').text.strip()
        sub_header = listing.find(class_='sub_head_inner_header')
        categories_in_header = sub_header.find_all('a')
        if len(categories_in_header) == 2:
            result['Category'] = categories_in_header[-1].find('h3').text.strip()
        else:
            part1 = categories_in_header[-2].find('h3').text.strip()
            part2 = categories_in_header[-1].find('h3').text.strip()
            result['Category'] = f'{part1} - {part2}'
        result['Amount Sold'] = int(list_desc.find('span').text.split('sold since')[0].strip())
        sold_since_str = list_desc.find('span').text.split('sold since')[1].strip()
        sold_since_dt = dt.datetime.strptime(sold_since_str, '%b %d, %Y').date()
        result['Sold Since'] = sold_since_dt

        # Get trust levels
        levels = list_desc.find_all('span', class_='levelSet')
        result['Vendor Level'] = int(''.join(char for char in levels[0].text.strip() if char.isdigit()))
        result['Trust Level'] = int(''.join(char for char in levels[1].text.strip() if char.isdigit()))

        # Get table content
        list_desc_content = list_desc.find_all('td')
        result['Product Class'] = list_desc_content[1].text.strip()
        result['Origin Country'] = list_desc_content[3].text.strip()
        quantity_left = list_desc_content[5].text.strip()
        result['Quantity Left'] = quantity_left
        result['Ships To'] = list_desc_content[7].text.strip()
        result['Ends In'] = list_desc_content[9].text.strip()
        result['Payment'] = list_desc_content[11].text.strip()

        if quantity_left != 'Sold Out':
            # Get prices if product is not sold out
            result['Price USD'] = list_desc.find(class_='padp').text.split('USD')[-1].strip()
            result['Price BTC'] = list_desc.find(class_='productcrypto').text.split('BTC')[0].strip()
        else:
            result['Price USD'] = 'Sold Out'
            result['Price BTC'] = 'Sold Out'

        # Get full description and specify correct datatype (string)
        result['Listing Description'] = str(listing.find(class_='tabcontent'))
        return result

    def parse_seller(self, file: Path) -> pd.Series:
        """
        Method that scrapes the given seller and returns a pandas Series with the scraped results
        :param file: Path of the html file to be parsed
        :return: pd.Series with the scraped results
        """

        # Create empty Series to store results in
        result = pd.Series(dtype='object')

        # Load html file
        seller = self.open_html(file)

        # Select most important info element on page
        seller_desc = seller.find(class_='right-content')
        result['Seller Name'] = seller_desc.find('h1').text.split('|')[0].strip()
        member_since = seller_desc.find(text=lambda text: 'Member since' in text).parent.text.split(':')[-1].strip()
        result['Member Since'] = member_since
        last_online_str = seller_desc.find(text=lambda text: 'Last online' in text).parent.text.split(':')[-1].strip()
        last_online_dt = dt.datetime.strptime(last_online_str, '%b %d, %Y').date()
        result['Last Online'] = last_online_dt
        user_info = seller.find(class_='user_info_mid_head')

        result['Seller Name'] = user_info.text.split('(')[0].strip()
        result['Seller Number'] = int(user_info.find_all('span')[0].text.strip()[1:-1])
        levels = user_info.find_all('span', class_='user_info_trust')
        result['Vendor Level'] = ''.join(char for char in levels[0].text.strip() if char.isdigit())
        result['Trust Level'] = ''.join(char for char in levels[1].text.strip() if char.isdigit())

        seller_rating = seller_desc.find(class_='seller_rating').find('table').find_all('td')
        result['Positive Feedback (12 months)'] = int(seller_rating[3].text.strip())
        result['Neutral Feedback (12 months)'] = int(seller_rating[7].text.strip())
        result['Negative Feedback (12 months)'] = int(seller_rating[11].text.strip())
        rating_star = seller_desc.find(class_='rating_star').find('table').find_all('td')
        result['Stealth Rating'] = float(rating_star[2].text.strip())
        result['Quality Rating'] = float(rating_star[3].text.strip())
        result['Delivery Rating'] = float(rating_star[4].text.strip())
        result['Seller Description'] = str(seller.find(class_='tabcontent_user_feedback'))
        return result

    def save_as_parquet(self):
        """
        Method that saves the results as a parquet file
        """

        logging.info('Writing files to disk as parquet (gzip) files.')

        # Reset indexes
        self.listings.reset_index(inplace=True, drop=True)
        self.sellers.reset_index(inplace=True, drop=True)

        # Save to disk
        self.listings.to_parquet(self.listings_save_location, engine='pyarrow', compression='gzip')
        self.sellers.to_parquet(self.sellers_save_location, engine='pyarrow', compression='gzip')

    def save_to_sql_db(self):
        """
        Method that stores the results in a SQL database
        """

        # Create database connection and write dataframes to database
        logging.info('Storing results in SQL Database.')
        db_connection = DbConnection()
        db_connection.write_data(relation_name='listings', rows_to_add=self.listings)
        db_connection.write_data(relation_name='sellers', rows_to_add=self.sellers)

    @staticmethod
    def open_html(file: Path) -> BeautifulSoup:
        """
        Method that reads in a html_file and returns a BeautifulSoup object
        :param file: file Path
        :return: BeautifulSoup object
        """

        with open(file, 'r') as file:
            raw_file = file.read()
        soup = BeautifulSoup(raw_file, 'html.parser')
        return soup

    @staticmethod
    def process_input_date(raw_input: str) -> dt.date:
        """
        Method that converts the input-string to a dt.date object. Defaults to dt.date.today if raw_input is None
        :param raw_input: string with input_date
        :return: formatted date as dt.date object
        """
        if not raw_input:
            return dt.date.today()
        else:
            date_elements = [int(elem) for elem in raw_input.split('-')]
            day, month, year = date_elements[0], date_elements[1], date_elements[2]
            return dt.date(year, month, day)
