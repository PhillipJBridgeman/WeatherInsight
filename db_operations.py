'''
db_operations.py

Description: This script will handle all database operations for the weather application.
Author: Phillip Bridgeman
Date: November 17, 2024
Last Modified: November 17, 2024
Version: 1.0
'''
import os
import sqlite3
try:
    from dbcm import DBCM
except ImportError:
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from dbcm import DBCM

class DBOperations:
    '''
    DBOperations class to handle all database operations.
    '''
    def __init__(self, db_name="weather_data.db"):
        self.db_name = db_name

    def initialize_db(self):
        """Initialize the database and create the table if it doesn't exist."""
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
        :param weather_data: Dictionary of weather data (date -> {Max, Min, Mean})
        :param location: Location name (default is Winnipeg)
        """
        with DBCM(self.db_name) as cursor:
            for sample_date, temps in weather_data.items():
                try:
                    cursor.execute("""
                        INSERT INTO weather (sample_date, location, min_temp, max_temp, avg_temp)
                        VALUES (?, ?, ?, ?, ?)
                    """, (sample_date, location, temps["Min"], temps["Max"], temps["Mean"]))
                except sqlite3.IntegrityError:
                    pass

    def fetch_data(self):
        """
        Fetch all weather data from the database.
        :return: List of rows containing weather data.
        """
        with DBCM(self.db_name) as cursor:
            cursor.execute(
                """SELECT sample_date,
                location, min_temp,
                max_temp, 
                avg_temp
                FROM weather"""
                )
            return cursor.fetchall()

    def purge_data(self):
        """Delete all weather data from the database without dropping the table."""
        with DBCM(self.db_name) as cursor:
            cursor.execute("DELETE FROM weather")
