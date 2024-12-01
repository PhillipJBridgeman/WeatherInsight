'''
dbcm.py

Description: A context manager module to manage SQLite database connections.
Author: Phillip Bridgeman
Date: November 17, 2024
Last Modified: November 22, 2024
Version: 1.2
'''

import sqlite3

class DBCM:
    """
    Context manager for SQLite database connections.
    Returns a cursor for executing SQL commands.
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.connection.commit()
        else:
            print(f"Database error: {exc_value}")
        self.cursor.close()
        self.connection.close()
