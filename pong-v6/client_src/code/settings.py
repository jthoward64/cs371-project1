# =================================================================================================
# Contributing Authors:	    Michael Stacy, Name Here, Name Here
# Email Addresses:          jmst231@uky.edu, Email Here, Email Here
# Date:                     October 29th, 2023
# Purpose:                  A configuration file for the Server Source
# Misc:                     Main  Configuration File
#                           Documentation for Port Ranges: https://learn.microsoft.com/en-us/mem/configmgr/core/plan-design/hierarchy/ports
# =================================================================================================

from socket import AF_INET, SOCK_STREAM
from json import JSONDecodeError

# Settings Folder to Contain Globals
MAIN_ADDRESS:str = 'localhost'
MAIN_PORT:int = 4000
RECEIVER_SIZE:int = 1024

# Settings for the Server Creation
ADDRESS_FAMILY = AF_INET # IPv4
SOCKET_KIND = SOCK_STREAM # TCP

# Settings for the Server Encryption
CERTFILE:str='./certs/cert.pem'

# Error List for Connections
ERROR_LIST:set = {BrokenPipeError, EOFError, ConnectionError, JSONDecodeError, UnicodeDecodeError}