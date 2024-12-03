'''
db_operations.py

Description: Handles all database operations for the weather application.
Author: Phillip Bridgeman
Date: November 17, 2024
Last Modified: December 3, 2024
Version: 1.3
'''

import sqlite3
import os
from dbcm import DBCM


class DBOperations:
    """
    DBOperations class to handle all database operations.
    """

    def __init__(self, db_name="weather_data.db"):
        """
        Initialize the database path. The database file will be stored in the user's
        local application data folder to ensure write permissions.
        """
        app_data_dir = os.getenv("LOCALAPPDATA", os.getcwd())
        self.db_name = os.path.join(app_data_dir, db_name)

        if not os.path.exists(app_data_dir):
            os.makedirs(app_data_dir)

    def initialize_db(self):
        """
        Initialize the database and create the table if it doesn't exist.
        """
        print(f"Initializing database at: {self.db_name}")
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
                    continue

    def update_data(self, weather_data, location="Winnipeg"):
        """
        Update weather data in the database.
        :param weather_data: Dictionary of weather data (date -> {Max, Min, Mean})
        :param location: Location name (default: Winnipeg)
        """
        with DBCM(self.db_name) as cursor:
            for sample_date, temps in weather_data.items():
                try:
                    cursor.execute("""
                        UPDATE weather
                        SET min_temp = ?, max_temp = ?, avg_temp = ?
                        WHERE sample_date = ? AND location = ?
                    """, (temps["Min"], temps["Max"], temps["Mean"], sample_date, location))
                except sqlite3.IntegrityError:
                    continue

    def fetch_data(self, filter_type="raw", year_range=None, year=None, month=None):
        """
        Fetch weather data from the database based on the filter type and parameters.
        """
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
            return cursor.fetchall()

    def purge_data(self):
        """
        Delete all weather data from the database without dropping the table.
        """
        with DBCM(self.db_name) as cursor:
            cursor.execute("DELETE FROM weather")

    def get_latest_date(self, location="Winnipeg"):
        """
        Fetch the latest date from the database for the given location.

        :param location: Location name (default: Winnipeg)
        :return: Latest date as a string (YYYY-MM-DD) or None if no records exist.
        """
        with DBCM(self.db_name) as cursor:
            cursor.execute("""
                SELECT MAX(sample_date)
                FROM weather
                WHERE location = ?
            """, (location,))
            result = cursor.fetchone()
            return result[0] if result and result[0] else None


if __name__ == "__main__":
    db = DBOperations()
    db.initialize_db()
    print("Database initialized successfully.")
