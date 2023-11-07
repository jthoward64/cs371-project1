# =================================================================================================
# Contributing Authors:	    Michael Stacy, Tag Howard, Juliann Hyatt
# Email Addresses:          jmst231@uky.edu, jtho264@uky.edu, jnhy222@uky.edu
# Date:                     October 29th, 2023
# Purpose:                  A configuration file for the Server Source
# Misc:                     Main  Configuration File
#                           Documentation for Port Ranges: https://learn.microsoft.com/en-us/mem/configmgr/core/plan-design/hierarchy/ports
# =================================================================================================

from socket import AF_INET, SOCK_STREAM

# Settings Folder to Contain Globals
MAIN_ADDRESS: str = "localhost"
MAIN_PORT: int = 4000
RECEIVER_SIZE: int = 1024

# The range of acceptable ports
LOWER_PORT: int = 49152
UPPER_PORT: int = 65535

# Settings for the Server Creation
ADDRESS_FAMILY = AF_INET
SOCKET_KIND = SOCK_STREAM

# Settings for the Server Encryption
CERTFILE: str = "./certs/cert.pem"
KEYFILE: str = "./certs/key.pem"
PASSWORD: str = ""  # Removed for Security Reasons
