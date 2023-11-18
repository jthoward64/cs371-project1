# =================================================================================================
# Contributing Authors:	    Tag Howard, John Michael Stacy, Juliann Hyatt
# Email Addresses:          jtho264@uky.edu, jmst231@uky.edu, jnhy222@uky.edu
# Date:                     November 7th, 2023
# Purpose:                  Serve leaderboard JSON to the client
# Misc:
# =================================================================================================

from http.server import HTTPServer, SimpleHTTPRequestHandler
from os import path

helpers_dir = path.abspath(path.dirname(__file__))
html_dir = path.join(helpers_dir, "HTML")

# Author:        Tag Howard
# Purpose:       To serve the Leaderboard
# Pre:           HTTPServer
# Post:          None
class Leaderboard(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=html_dir, **kwargs)


if __name__ == "__main__":
    with HTTPServer(("0.0.0.0", 80), Leaderboard) as httpd:
        print("serving leaderboard.html at port", 80)
        httpd.serve_forever()
