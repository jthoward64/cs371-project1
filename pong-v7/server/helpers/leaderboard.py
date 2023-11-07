# =================================================================================================
# Contributing Authors:	    Tag Howard, Name Here, Name Here
# Email Addresses:          jtho264@uky.edu, Email Here, Email Here
# Date:                     November 7th, 2023
# Purpose:                  Serve ../HTML/leaderboard.html to the client
# Misc:
# =================================================================================================

import json
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from os import path

from .database import Database

helpers_dir = path.abspath(path.dirname(__file__))
html_dir = path.join(helpers_dir, "../HTML")


class Leaderboard(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=html_dir, **kwargs)


class LeaderboardApi(BaseHTTPRequestHandler):
    def do_GET(self):
        """Returns the Top 10 Leaderboard"""
        db = Database()

        data = db.grab_leaderboard()
        if data is None:
            print("Error: No leaderboard data")
            data = {}

        str = json.dumps(data)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(str.encode())
        return


def run_server():
    with HTTPServer(("", 80), Leaderboard) as httpd:
        print("serving leaderboard.html at port", 80)
        httpd.serve_forever()
    with HTTPServer(("", 8500), LeaderboardApi) as httpd:
        print("serving leaderboard API at port", 8500)
        httpd.serve_forever()
