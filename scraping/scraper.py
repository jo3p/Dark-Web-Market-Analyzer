from bs4 import BeautifulSoup
from pathlib import Path
import os
import datetime as dt
import pandas as pd


class DocumentParser:
    def __init__(self, scrape_date: dt.date):
        # Define the folder structure
        self.work_dir = Path(os.getcwd())
        self.scrape_date = str(scrape_date)
        self.scrape_dir = self.work_dir / 'data' / self.scrape_date
        self.listings_dir = self.scrape_dir / 'listings'
        self.sellers_dir = self.scrape_dir / 'sellers'
        self.listings_save_location = self.scrape_dir / 'scraped_listings.gzip'

        # Define an attribute for the final result
        self.listings = pd.DataFrame()
        self.sellers = pd.DataFrame()

    def scrape(self):
        """
        Method that initiates the parsing of listings and sellers and appends the results to the corresponding dataframe
        """

        # # scrape sellers
        # for file in os.listdir(self.sellers_dir):
        #     seller = self.parse_seller(self.sellers_dir / file)
        #     self.sellers = pd.concat([self.sellers, seller.to_frame().T])

        # scrape listings
        for file in os.listdir(self.listings_dir):
            listing = self.parse_listing(self.listings_dir / file)
            self.listings = pd.concat([self.listings, listing.to_frame().T])

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
        list_des = listing.find(class_='listDes')

        # Get general stats  # TODO: Find category as well
        result['Seller Name'] = list_des.find('b').find('a').text.strip()
        result['Scrape Date'] = self.scrape_date
        result['Title'] = list_des.find('h2').text.strip()
        result['Amount Sold'] = int(list_des.find('span').text.split('sold since')[0].strip())
        result['Sold since'] = list_des.find('span').text.split('sold since')[1].strip()

        # Get trust levels
        levels = list_des.find_all('span', class_='levelSet')
        result['Vendor Level'] = ''.join(char for char in levels[0].text.strip() if char.isdigit())
        result['Trust Level'] = ''.join(char for char in levels[1].text.strip() if char.isdigit())

        # Get table content
        list_des_content = list_des.find_all('td')
        result['Product Class'] = list_des_content[1].text.strip()
        result['Origin Country'] = list_des_content[3].text.strip()
        result['Quantity Left'] = int(list_des_content[5].text.strip())
        result['Ships to'] = list_des_content[7].text.strip()
        result['Ends in'] = list_des_content[9].text.strip()
        result['Payment'] = list_des_content[11].text.strip()

        # Get prices
        result['Price USD'] = float(list_des.find(class_='padp').text.split('USD')[-1].strip())
        result['Price BTC'] = float(list_des.find(class_='productcrypto').text.split('BTC')[0].strip())

        # Get full description and specify correct datatype (string)
        result['Description'] = listing.find(class_='tabcontent').find('p')
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

        return result

    def save_as_parquet(self):
        """
        Method that saves the results as a parquet file
        """

        # Set correct datatype and save to disk
        self.listings = self.listings.astype({'Description': 'str'})
        self.listings.to_parquet(self.listings_save_location, engine='pyarrow', compression='gzip')

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


if __name__ == '__main__':
    parser = DocumentParser(dt.date.today())
    parser.scrape()
    parser.save_as_parquet()
    test_df_listings = pd.read_parquet(parser.listings_save_location)
