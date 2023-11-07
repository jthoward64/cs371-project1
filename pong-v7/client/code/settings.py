# =================================================================================================
# Contributing Authors:	    Michael Stacy, Juliann Hyatt, Name Here
# Email Addresses:          jmst231@uky.edu, jnhy222@uky.com, Email Here
# Date:                     October 29th, 2023
# Purpose:                  A way to create an encrypted Server Socket for Games and Main Server
# Misc:                     Documentation: https://docs.python.org/3/library/ssl.html
# =================================================================================================

from socket import AF_INET, SOCK_STREAM

# Settings Folder to Contain Globals
MAIN_ADDRESS:str = 'localhost'
MAIN_PORT:int = 4000
RECEIVER_SIZE:int = 1024

# Settings for the Server Creation
ADDRESS_FAMILY = AF_INET # IPv4
SOCKET_KIND = SOCK_STREAM # TCP

# Settings for the Server Encryption
CERTFILE:str='./certs/cert.pem'

