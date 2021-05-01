# Dark-Web-Market-Analyzer

The goal of this project was to crawl and scrape information from a Dark Web Marketplace, to extract useful insights.
The project comes with a Pipfile, meaning that the environment can be set up automatically. There are
two access point to the main functionality code: execute crawler.py and execute scraper.py. The first script
executes the crawling process. It relies mainly on two classes files: driver.py and crawler.py. driver.py
contains the WebDriver class, which contains all necessary information to instantiate a web-driver instance.
crawler.py , container the WebCrawler class, inherits functionality from the WebDriver. The class instantiates
a WebDriver object and iteratively visits listing and vendor pages on the marketplace and saves them to disk.
The second access point (execute scraper.py) executes the scraping process, it mainly relies on scraper.py
(class DocumentParser). The results are written both to disk (as a parquet file) and to the SQL database.
For the latter process, the database.py file is consulted.

The code depends on a number of factors, which are stated here for reproduction purposes. First, the
Selenium web-driver requires a Firefox and Tor installation. Furthermore, in the create driver function
from the WebDriver class, a path to the torrc file is set (i.e. ’/etc/tor/’). This might need to be changed,
depending on where TOR is installed. Additionally, the Firefox profile parameters are saved in a JSON file.
Users might need to adapt these to correctly configure the web-driver.
In addition, the code depends on the ODBC drivers for SQL servers on Linux to connect to the database.
The drivers can be installed with help of this tutorial (for Ubuntu).
Lastly, a number of environment variables are utilized to log into the marketplace and database. These
should be replaced with the credentials of the user.

Please note that browsing the Dark Web can be dangerous. Implement proper security precautions before executing this code. 
