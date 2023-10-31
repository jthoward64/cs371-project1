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

class Entity:
    username:Optional[str] = None
    password:Optional[str] = None
    initials:Optional[str] = None
    wins:int = 0

class Connection:
    def __init__(self) -> None:
        try:
            self.connection = connector.connect(DATABASE_PATH)
        except Error as e:
            print('Database Error: ', e)

        self.cursor = self.connection.cursor()

    def close(self) -> None:
        self.cursor.close()
        self.connection.close()
        
    def grab_entity(self, username:str) -> Optional[Entity]:
        '''Grabs the Entity Object from the Database'''

        # Our select statement
        new_query = 'SELECT password, initials, wins FROM users WHERE username = ?'

        # Execute the query
        self.cursor.execute(new_query, (username,))

        # Grab our result from the execution
        result = self.cursor.fetchone()
        if result:
            entity = Entity()
            entity.username = username
            entity.password, entity.initials, entity.wins = result
            return entity
        
        return None
    
    def create_entity(self, entity:Entity) -> bool:
        '''Attempts to create a new entity'''

        insert_query = 'INSERT INTO users (username, password, initials, wins) VALUES (?, ?, ?, ?)'

        try:
            self.cursor.execute(insert_query, (entity.username, entity.password, entity.initials, entity.wins))
            self.connection.commit()
            return True
        except Error:
            print('Failed to create user')

            # Rollback in the event of an error
            self.connection.rollback()
            return False

    def update_entity(self, entity:Entity) -> bool:
        '''Attempts to Update the Entity Object in the Database'''
        try:
            # New Query
            update_query = 'UPDATE users SET wins = ? WHERE username = ?'

            # Execute and Commit
            self.cursor.execute(update_query, (entity.wins, entity.username))
            self.connection.commit()

            return True
        except Error:
            # Failed
            print('Failed to Update')
            self.connection.rollback()

            return False

class Database:
    def __init__(self) -> None:
        # Create our cursor
        self.__database:Connection = Connection()

        self.entity:Entity = Entity()

    def close(self) -> None:
        '''Closes the Database'''
        self.__database.close()

    def validate_user(self, username:str, password:str) -> Tuple[bool, Optional[str]]:
        '''Validates if an Entity Exists and the Password Matches'''

        # Grab the Entity
        entity = self.__database.grab_entity(username)

        # Does the entity exists
        if not entity:
            return False, 'Account does not exists'
        
        # Does the password match?
        if not entity.password == password:
            return False, 'Incorrect Password'

        # Valid user
        self.entity = entity

        return True, None

    def create_user(self, username:str, password:str, initials:str) -> bool:
        '''Creates a New Entity'''

        # Ensure Entity does not exists
        if self.entity:
            return False

        # New Entity, Set Password and Username
        entity = Entity()  
        entity.username = username
        entity.password = password
        entity.initials = initials

        # Return Commit Result
        return self.__database.create_entity(entity)

    def increment_win(self, username:str) -> bool:
        '''Increments the Win Attribute'''

        # Ensure entity does exists
        if not self.entity:
            return False

        # Increments a win for the user
        self.entity.wins += 1

        # See if our commit succeeded
        success = self.__database.update_entity(self.entity)
        if not success:
            # Undo our addition
            self.entity.wins -= 1
            return False
        
        return True
