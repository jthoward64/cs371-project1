from flask import Flask, jsonify
from flask_cors import CORS

# This is to enable CORS for the routes to leaderboard.py
app = Flask(__name__)
CORS(app)

from helpers.database import Database

@app.route('/leaderboard', methods=['GET'])
def grab_leaderboard():
    '''Returns the Top 10 Leaderboard'''
    db = Database()

    data = db.grab_leaderboard()
    if data is None:
        print('Error: No leaderboard data')
        data = {}

    return jsonify(data)

if __name__ == '__main__':
    # Set our port to 8500 and on IP localhost
    app.run(host='localhost', port=8500)



