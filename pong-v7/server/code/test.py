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
        
    def increment_wins(self, username:str, wins:int) -> Tuple[bool, str]:
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