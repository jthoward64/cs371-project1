# =================================================================================================
# Contributing Authors:	    Michael Stacy, Tag Howard, Juliann Hyatt
# Email Addresses:          jmst231@uky.edu, jtho264@uky.edu, jnhy222@uky.edu
# Date:                     October 29th, 2023
# Purpose:                  A configuration file for the Server Source
# Misc:                     Main  Configuration File
#                           Documentation for Port Ranges: https://learn.microsoft.com/en-us/mem/configmgr/core/plan-design/hierarchy/ports
# =================================================================================================

from os import path
from socket import AF_INET, SOCK_STREAM

# Settings Folder to Contain Globals
MAIN_ADDRESS: str = "0.0.0.0"
MAIN_PORT: int = 4000
RECEIVER_SIZE: int = 1024

# The range of acceptable ports
LOWER_PORT: int = 15000
UPPER_PORT: int = 16000

# Settings for the Server Creation
ADDRESS_FAMILY = AF_INET
SOCKET_KIND = SOCK_STREAM

# Settings for the Server Encryption
current_dir = path.abspath(path.dirname(__file__))
CERTFILE: str = path.join(current_dir, "..", "certs", "cert.pem")
KEYFILE: str = path.join(current_dir, "..", "certs", "key.pem")
PASSWORD: str = "buxbor-dasjyR-8koqvi"  # Removed for Security Reasons
