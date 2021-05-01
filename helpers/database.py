import urllib
import pandas as pd
import pyodbc
import sqlalchemy
import os
from pathlib import Path


class DbConnection:
    """
    Class that handles the connection to the SQL Server in Google Cloud
    """
    def __init__(self):
        # set connection parameters
        self.driver = 'ODBC Driver 17 for SQL Server'
        self.server_url = os.environ['server_url']
        self.database = 'scraped_data'
        self.db_username = 'sqlserver'
        self.db_password = os.environ['db_password']
        self.connection_string = f'DRIVER={self.driver};' \
                                 f'SERVER={self.server_url};' \
                                 f'DATABASE={self.database};' \
                                 f'UID={self.db_username};' \
                                 f'PWD={self.db_password}'

        self.safe_url = urllib.parse.quote(self.connection_string)  # convert special characters and spaces etc.
        self.engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=" + self.safe_url)

    def write_data(self, relation_name: str, rows_to_add: pd.DataFrame):
        """
        Method that appends "rows_to_add" to database "relation_name"
        :param relation_name: relation name that is appended to
        :param rows_to_add: pandas DataFrame that contains entries to be added to the relation
        :return: nothing
        """

        rows_to_add.to_sql(name=relation_name,
                           con=self.engine,
                           if_exists='append',
                           index=False)

    def test_db_connection(self, relation_name: str, sql_query_path: Path = None) -> pd.DataFrame:
        """
        Method to test the connection to the database
        :param sql_query_path: optional parameter to insert a SQL query file
        :param relation_name: the relation to query from
        :return: Pandas DataFrame that contains
        """

        # open SQL query file if given as parameter
        if sql_query_path:
            with open(sql_query_path) as file:
                query = file.read()
        else:
            query = f"SELECT * FROM {relation_name}"

        # execute query
        with pyodbc.connect(self.connection_string) as connection:
            return pd.read_sql(query, connection)


if __name__ == '__main__':
    # Initialize db connection
    db_connection = DbConnection()

    # Retrieve a test-query from the database to test the connection
    testresult = db_connection.test_db_connection(relation_name='listings')
