'''
Module: dbcm
Description: This module provides a context manager for database connections.
Author: Phillip Bridgeman
Date: November 17, 2024
Last Modified: November 17, 2024
Version: 1.0
'''
import sqlite3

class DBCM:
    '''
    Context manager for database connections.
    '''
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()
