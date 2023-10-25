# Documentation Credit: https://downloads.mysql.com/docs/connector-python-en.pdf

from dbConfiguration import dbInformation
from typing import Optional, Tuple, Union, List

# For connecting SQL
import mysql.connector as connector
from mysql.connector import errorcode

# For Type Hinting
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor


class Database:
    def __init__(self) -> None:
        # Open the connection
        self.openConnection()

    def closeConnection(self) -> None:
        if self.Connection:
            self.Connection.close()

    def openConnection(self) -> None:
        # Grab our new connection and grab the cursosr
        try:
            self.Connection = connector.connect(**dbInformation)
        except connector.Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Database Access Denied')
            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                print('Database does not exist')
            else:
                print(e)
            return
        
        self.Cursor = self.Connection.cursor()

    def fetchData(self, table:Optional[str]=None, comparisonLogic:Optional[str]=None, returnAttributes:Optional[str]=None, orderBy:Optional[str]=None, direction:Optional[str]=None, multiple:bool=False) -> Union[Tuple, List[Tuple], None]:
        # Check if the connection is open 
        if not self.Cursor or not  self.Connection:
            return None
        
        # Ensure we have a returnAttributes and table
        if not returnAttributes or not table:
            print('No table or selected attributes requested')
            return None
        
        # Create our new query
        newQuery = f"SELECT {returnAttributes} FROM {table}"

        if comparisonLogic:
            newQuery += f" WHERE {comparisonLogic}"
        
        if orderBy and direction:
            newQuery += f" ORDER BY {orderBy} {direction}"

        newQuery += ";"

        # Execute our query, grab our data
        self.Cursor.execute(newQuery)

        if multiple:
            newData = self.Cursor.fetchall()
        else:
            newData = self.Cursor.fetchone()
        return newData
    
    def insertData(self, table:str, information:dict={}) -> Union[bool, None]:
        # Check if the connection is open 
        if not self.Cursor or not  self.Connection:
            return None
        
        # Check if dict is empty
        if not information:
            return False
        
        # Grab all the attributes and give a %s placeholder for each one
        attributes = ', '.join(information.keys())
        placeHolder = ', '.join(['%s'] * len(information))

        # Our query
        newQuery = f'INSERT INTO {table} ({attributes}) VALUES ({placeHolder});'

        # Attempt the transaction
        try:
            self.Cursor.execute(newQuery, tuple(information.values()))
            self.Connection.commit()
            return True
        except connector.Error as errorInfo:
            print(f'Transaction Failed: {errorInfo}')
            return False