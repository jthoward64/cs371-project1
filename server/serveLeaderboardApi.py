# =================================================================================================
# Contributing Authors:	    Tag Howard, John Michael Stacy, Juliann Hyatt
# Email Addresses:          jtho264@uky.edu, jmst231@uky.edu, jnhy222@uky.edu
# Date:                     November 7th, 2023
# Purpose:                  Serve leaderboard JSON to the client
# Misc:
# =================================================================================================

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path

from helpers.database import Database

# Author:        Tag Howard
# Purpose:       To serve the Leaderboard
# Pre:           HTTPServer
# Post:          None
class LeaderboardApi(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        """Returns the Top 10 Leaderboard"""
        db = Database()

        data = db.grab_leaderboard()
        if data is None:
            print("Error: No leaderboard data")
            data = {}

        str = json.dumps(data)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(str.encode())
        return


if __name__ == "__main__":
    with HTTPServer(("", 8500), LeaderboardApi) as httpd:
        print("serving leaderboard API at port", 8500)
        httpd.serve_forever()
