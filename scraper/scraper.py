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
        result = pd.Series(dtype='object')
        html_doc = self.open_html(file)
        result['Title'] = html_doc.title.text
        result['Seller_name'] = html_doc.find(class_='seth1')  # TODO: uitzoeken waarom dit niet werkt
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
thing = parser.parse_listing(parser.file_path)
