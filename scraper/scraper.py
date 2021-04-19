from bs4 import BeautifulSoup
from pathlib import Path
import os
import datetime as dt
import pandas as pd


class DocumentParser:
    def __init__(self):
        self.work_dir = Path(os.getcwd())
        self.today = str(dt.date.today())
        self.listings_dir = self.work_dir/'data'/self.today/'listings'
        self.filename = os.listdir(self.listings_dir)[0]  # TODO: make for-loop
        self.file_path = self.listings_dir/self.filename

    def parse_listing(self, file: Path):
        # Create empty Series to store results in
        result = pd.Series(dtype='object')

        # Load html file
        html_doc = self.open_html(file)

        # Select most important info element on page
        list_des = html_doc.find(class_='listDes')

        # Get general stats
        result['Seller Name'] = list_des.find('b').find('a').text.strip()
        result['Scrape Date'] = self.today
        result['Title'] = list_des.find('h2').text.strip()
        result['Amount Sold'] = int(list_des.find('span').text.split('sold since')[0].strip())
        result['Sold since'] = list_des.find('span').text.split('sold since')[1].strip()

        # Get trust levels
        levels = list_des.find_all('span', class_='levelSet')  # TODO: check .find(text='Vendor')
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

        # Get full description
        result['Description'] = html_doc.find(class_='tabcontent').find('p')
        return result

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


parser = DocumentParser()
to_add = parser.parse_listing(parser.file_path)

