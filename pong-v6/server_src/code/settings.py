# =================================================================================================
# Contributing Authors:	    Michael Stacy
# Email Addresses:          jmst231@uky.edu
# Date:                     October 26th, 2023
# Purpose:                  A configuration file for the Server Source
# Misc:                     Main  Configuration File
#                           Random Port: https://learn.microsoft.com/en-us/mem/configmgr/core/plan-design/hierarchy/ports
# =================================================================================================

from socket import AF_INET, SOCK_STREAM
from json import JSONDecodeError

# Settings Folder to Contain Globals
MAIN_ADDRESS:str = 'localhost'
MAIN_PORT:int = 4000
RECEIVER_SIZE:int = 1024

# The range of acceptable ports
LOWER_PORT:int = 49152
UPPER_PORT:int = 65535

# Settings for the Server Creation
ADDRESS_FAMILY = AF_INET
SOCKET_KIND = SOCK_STREAM

# Settings for the Server Encryption
CERTFILE:str='../certs/cert.pem'
KEYFILE:str='../certs/key.pem'
PASSWORD:str='' # Removed for Security Reasons

# Settings for the Database
CONFIG:dict = {
    'host': 'mysql.cs.uky.edu',
    'user': '', # Removed for Security Reasons
    'password': '', # Removed for Security Reasons
    'database': 'CS371',
}

ERROR_LIST:set = {BrokenPipeError, EOFError, ConnectionError, JSONDecodeError, UnicodeDecodeError}