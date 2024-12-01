'''
db_operations.py

Description: Handles all database operations for the weather application.
Author: Phillip Bridgeman
Date: November 17, 2024
Last Modified: November 22, 2024
Version: 1.2
'''

import sqlite3
from dbcm import DBCM

class DBOperations:
    """
    DBOperations class to handle all database operations.
    """
    def __init__(self, db_name="weather_data.db"):
        '''
        Initialize the database name.
        '''
        self.db_name = db_name

    def initialize_db(self):
        """
        Initialize the database and create the table if it doesn't exist.
        """
        with DBCM(self.db_name) as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sample_date TEXT NOT NULL,
                    location TEXT NOT NULL,
                    min_temp REAL,
                    max_temp REAL,
                    avg_temp REAL,
                    UNIQUE(sample_date, location)
                )
            """)

    def save_data(self, weather_data, location="Winnipeg"):
        """
        Save weather data to the database.
        Prevents duplication using UNIQUE constraints.

        :param weather_data: Dictionary of weather data (date -> {Max, Min, Mean})
        :param location: Location name (default: Winnipeg)
        """
        with DBCM(self.db_name) as cursor:
            for sample_date, temps in weather_data.items():
                try:
                    cursor.execute("""
                        INSERT INTO weather (sample_date, location, min_temp, max_temp, avg_temp)
                        VALUES (?, ?, ?, ?, ?)
                    """, (sample_date, location, temps["Min"], temps["Max"], temps["Mean"]))
                except sqlite3.IntegrityError:
                    # Skip duplicates
                    continue

    def fetch_data(self, filter_type="raw", year_range=None, year=None, month=None):
        try:
            if filter_type == "raw":
                with DBCM(self.db_name) as cursor:
                    cursor.execute("SELECT * FROM weather")
                    return cursor.fetchall()
            elif filter_type == "boxplot" and year_range:
                start_year, end_year = year_range
                with DBCM(self.db_name) as cursor:
                    query = """
                        SELECT strftime('%m', sample_date) AS month, avg_temp
                        FROM weather
                        WHERE CAST(strftime('%Y', sample_date) AS INTEGER) BETWEEN ? AND ?
                    """
                    cursor.execute(query, (start_year, end_year))
                    return cursor.fetchall()
            elif filter_type == "lineplot" and year and month:
                with DBCM(self.db_name) as cursor:
                    query = """
                        SELECT strftime('%d', sample_date) AS day, avg_temp
                        FROM weather
                        WHERE CAST(strftime('%Y', sample_date) AS INTEGER) = ? 
                        AND CAST(strftime('%m', sample_date) AS INTEGER) = ?
                    """
                    cursor.execute(query, (year, month))
                    return cursor.fetchall()
            else:
                print("Invalid filter type or missing parameters.")
                return None
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            return None

    def fetch_all_data(self):
        """
        Fetch all data from the database.
        :return: Rows tuple containing all records.
        """
        with DBCM(self.db_name) as cursor:
            cursor.execute("SELECT * FROM weather")
            return cursor.fetchall()  # Explicitly return rows tuple

    def purge_data(self):
        """
        Delete all weather data from the database without dropping the table.
        """
        with DBCM(self.db_name) as cursor:
            cursor.execute("DELETE FROM weather")
