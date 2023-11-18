# =================================================================================================
# Contributing Authors:	    Michael Stacy, Tag Howard, Juliann Hyatt
# Email Addresses:          jmst231@uky.edu, jtho264@uky.edu, jnhy222@uky.edu
# Date:                     October 29th, 2023
# Purpose:                  How we connect to the Database in Multilabs
# Misc:                     Documentation: https://dev.mysql.com/doc/connector-python/en/connector-python-coding.html
# =================================================================================================

import sqlite3 as connector

# Needed to control the database
from os import path
from sqlite3 import Error

# For Type Hinting
from typing import Tuple, Union

current_dir = path.abspath(path.dirname(__file__))
DATABASE_PATH: str = path.join(current_dir, "..", "database", "holder.db")


class Database:
    # Author:        Michael Stacy
    # Purpose:       To establish our connection to the database
    # Pre:           None
    # Post:          None
    def __init__(self) -> None:
        # Create the Connector
        self._connect = connector.connect(DATABASE_PATH)

        print("Connected to Database")

    # Author:        Michael Stacy
    # Purpose:       Returns whether the Username and Password are correct
    # Pre:           String Username/Password
    # Post:          A success bool and string message
    def validate_user(self, username: str, password: str) -> Tuple[bool, str]:
        """Validates if a user exists and if the password is correct"""

        with self._connect as conn:
            cursor = conn.cursor()

            new_query = "SELECT password FROM users WHERE username = ?;"

            try:
                cursor.execute(new_query, (username,))
            except Error as new_error:
                print(f"Failed to validate: ", new_error)
                return False, "Failed to Validate"

            try:
                result = cursor.fetchone()
            except Error as new_error:
                print(f"Failed to fetch: ", new_error)
                return False, "Failed to Fetch"

            if result is None:
                return False, "Account does not exists"

            if result[0] != password:
                return False, "Incorrect Password"

            return True, "Success"

    # Author:        Michael Stacy
    # Purpose:       To create a new user account
    # Pre:           String Username/Password/Initials
    # Post:          A success and string message
    def create_user(
        self, username: str, password: str, initials: str
    ) -> Tuple[bool, str]:
        """Creates a new user from the given information"""
        with self._connect as conn:
            cursor = conn.cursor()

            new_query = "INSERT INTO users (username, password, initials, wins) VALUES (?, ?, ?, ?);"

            try:
                cursor.execute(new_query, (username, password, initials, 0))
                self._connect.commit()
            except Error as new_error:
                print(f"Failed to Create User: ", new_error)
                return False, "Failed to Create User"

            return True, "Success"
    
    # Author:        Michael Stacy
    # Purpose:       To grab the initials of the user
    # Pre:           String Username
    # Post:          Tuple success, message, and string of initial
    def grab_initial(self, username: str) -> Tuple[bool, str, str]:
        """Returns the number of wins currently in the database"""

        with self._connect as conn:
            cursor = conn.cursor()

            new_query = "SELECT initials FROM users WHERE username = ?;"

            try:
                cursor.execute(new_query, (username,))
            except Error as new_error:
                print(f"Failed to validate: ", new_error)
                return False, "Failed to Grab", ''

            try:
                result = cursor.fetchone()
            except Error as new_error:
                print(f"Failed to fetch: ", new_error)
                return False, "Failed to Fetch", ''

            if result is None:
                return False, "Initial does not exist", ''

            return True, "Success", result[0]

    # Author:        Michael Stacy
    # Purpose:       To update the number of wins of the user
    # Pre:           String Username, Int Wins
    # Post:          Success Bool, Message String
    def update_wins(self, username: str, wins: int) -> Tuple[bool, str]:
        """Increments the number of wins"""
        with self._connect as conn:
            cursor = conn.cursor()

            new_query = "UPDATE users SET wins = ? WHERE username = ?;"

            try:
                cursor.execute(new_query, (wins, username))
                self._connect.commit()
            except Error as new_error:
                print("Failed to increment wins: ", new_error)
                return False, "Failed to increment wins"

            return True, "Success"

    # Author:        Michael Stacy
    # Purpose:       To grab the number of wins
    # Pre:           String Username
    # Post:          Success Bool, String Message, Wins Int
    def grab_wins(self, username: str) -> Tuple[bool, str, int]:
        """Returns the number of wins currently in the database"""

        with self._connect as conn:
            cursor = conn.cursor()

            new_query = "SELECT wins FROM users WHERE username = ?;"

            try:
                cursor.execute(new_query, (username,))
            except Error as new_error:
                print(f"Failed to validate: ", new_error)
                return False, "Failed to Validate", 0

            try:
                result = cursor.fetchone()
            except Error as new_error:
                print(f"Failed to fetch: ", new_error)
                return False, "Failed to Fetch", 0

            if result is None:
                return False, "Account does not exists", 0

            return True, "Success", result[0]

    # Author:        Michael Stacy
    # Purpose:       To grab the top players of the database
    # Pre:           None
    # Post:          A dictionary of items or none
    def grab_leaderboard(self) -> Union[dict, None]:
        """Returns a Dictionary of Top Players"""
        with self._connect as conn:
            cursor = conn.cursor()

            new_query = "SELECT initials, wins FROM users ORDER BY wins DESC LIMIT 10;"

            try:
                cursor.execute(new_query)
            except Error as new_error:
                print(f"Failed to grab leaderboard: {new_error}")
                return None

            try:
                result = cursor.fetchall()
            except Error as new_error:
                print(f"Failed to fetch leaderboard: {new_error}")
                return None

            # Check if our result is None
            if result is None:
                print("Leaderboard does not exist")
                return None

            # Create a dictionary holder
            holder = {}

            # Conver the result into a dictionary
            for item in result:
                holder[item[0]] = item[1]

            return holder
