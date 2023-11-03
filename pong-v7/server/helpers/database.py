# =================================================================================================
# Contributing Authors:	    Michael Stacy, Name Here, Name Here
# Email Addresses:          jmst231@uky.edu, Email Here, Email Here
# Date:                     October 29th, 2023
# Purpose:                  How we connect to the Database in Multilabs
# Misc:                     Documentation: https://dev.mysql.com/doc/connector-python/en/connector-python-coding.html
# =================================================================================================

# Needed to control the database
import sqlite3 as connector
from sqlite3 import Error

# For Type Hinting
from typing import Tuple, Optional

DATABASE_PATH:str = './database/holder.db'

class Database:
    def __init__(self) -> None:
        # Create the Connector
        self._connect = connector.connect(DATABASE_PATH)

        print('Connected to Database')

    def validate_user(self, username:str, password:str) -> Tuple[bool, str]:
        '''Validates if a user exists and if the password is correct'''

        with self._connect as conn:

            cursor = conn.cursor()

            new_query = 'SELECT password FROM users WHERE username = ?;'
            
            try:
                cursor.execute(new_query, (username,))
            except Error as new_error:
                print(f'Failed to validate: ', new_error)
                return False, 'Failed to Validate'

            try:
                result = cursor.fetchone()
            except Error as new_error:
                print(f'Failed to fetch: ', new_error)
                return False, 'Failed to Fetch'
            
            if result is None:
                return False, 'Account does not exists'
            
            if result[0] != password:
                return False, 'Incorrect Password'
            
            return True, 'Success'
    
    def create_user(self, username:str, password:str, initials:str) -> Tuple[bool, str]:
        '''Creates a new user from the given information'''
        with self._connect as conn:

            cursor = conn.cursor()

            new_query = 'INSERT INTO users (username, password, initials, wins) VALUES (?, ?, ?, ?);'
            
            try:
                cursor.execute(new_query, (username, password, initials, 0))
                self._connect.commit()
            except Error as new_error:
                print(f'Failed to Create User: ', new_error)
                return False, 'Failed to Create User'

            return True, 'Success'
        
    def update_wins(self, username:str, wins:int) -> Tuple[bool, str]:
        '''Increments the number of wins'''
        with self._connect as conn:

            cursor = conn.cursor()

            new_query = 'UPDATE users SET wins = ? WHERE username = ?;'

            try:
                cursor.execute(new_query, (wins, username))
                self._connect.commit()
            except Error as new_error:
                print('Failed to increment wins: ', new_error)
                return False, 'Failed to increment wins'
            
            return True, 'Success'
        
    def grab_wins(self, username:str) -> Tuple[bool, str, int]:
        '''Returns the number of wins currently in the database'''

        with self._connect as conn:

            cursor = conn.cursor()

            new_query = 'SELECT wins FROM users WHERE username = ?;'
            
            try:
                cursor.execute(new_query, (username,))
            except Error as new_error:
                print(f'Failed to validate: ', new_error)
                return False, 'Failed to Validate', 0

            try:
                result = cursor.fetchone()
            except Error as new_error:
                print(f'Failed to fetch: ', new_error)
                return False, 'Failed to Fetch', 0
            
            if result is None:
                return False, 'Account does not exists', 0
            
            return True, 'Success', result[0]