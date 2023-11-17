# =================================================================================================
# Contributing Authors:	    Michael Stacy, Juliann Hyatt, Name Here
# Email Addresses:          jmst231@uky.edu, jnhy222@uky.com, Email Here
# Date:                     October 29th, 2023
# Purpose:                  A way to create an encrypted Server Socket for Games and Main Server
# Misc:                     Documentation: https://docs.python.org/3/library/ssl.html
# =================================================================================================

import argparse
from os import path
from socket import AF_INET, SOCK_STREAM

parser: argparse.ArgumentParser = argparse.ArgumentParser(
    description="Pong Lobby Server"
)
parser.add_argument(
    "--hostname",
    metavar="hostname",
    type=str,
    help="The hostname of the server",
    default="10.113.33.209",
)
parser.add_argument(
    "--port",
    metavar="port",
    type=int,
    help="The port number of the server",
    default=4000,
)

parser.add_argument(
    "--height",
    metavar="height",
    type=int,
    help="The height of the game window",
    default=480,
)
parser.add_argument(
    "--width",
    metavar="width",
    type=int,
    help="The width of the game window",
    default=640,
)

args: argparse.Namespace = parser.parse_args()

# Settings Folder to Contain Globals
MAIN_ADDRESS: str = args.hostname
MAIN_PORT: int = args.port
RECEIVER_SIZE: int = 1024

# Settings for the Server Creation
ADDRESS_FAMILY = AF_INET  # IPv4
SOCKET_KIND = SOCK_STREAM  # TCP

WINDOW_HEIGHT = args.height
WINDOW_WIDTH = args.width

# Settings for the Server Encryption
current_dir = path.abspath(path.dirname(__file__))
CERTFILE: str = path.join(current_dir, "..", "certs", "cert.pem")
