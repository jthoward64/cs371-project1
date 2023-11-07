# =================================================================================================
# Contributing Authors:	    Tag Howard, Name Here, Name Here
# Email Addresses:          jtho264@uky.edu, Email Here, Email Here
# Date:                     November 7th, 2023
# Purpose:                  Serve ../HTML/leaderboard.html to the client
# Misc:
# =================================================================================================

from http.server import HTTPServer, SimpleHTTPRequestHandler
from os import path

helpers_dir = path.abspath(path.dirname(__file__))
html_dir = path.join(helpers_dir, "HTML")


class Leaderboard(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=html_dir, **kwargs)


if __name__ == "__main__":
    with HTTPServer(("", 80), Leaderboard) as httpd:
        print("serving leaderboard.html at port", 80)
        httpd.serve_forever()
