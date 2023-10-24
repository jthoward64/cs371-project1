from flask import Flask, render_template_string
from handler.gameConfigure import leaderboardip, leaderboardport

webpage = Flask(__name__)

htmlCode = """
<!DOCTYPE html>
    <head>
        <title>Pong Leaderboard</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js"></script>
    </head>
    <body>
        <div class="ui segment">
            <h1 class="ui center aligned segment">Pong Leaderboard</h1>
            <button class="ui fluid primay button">
                <i class="redo icon"></i>Refresh
            </button>
        <div class="ui horizontal segments">
            <div class="ui segment">
                <div class="ui vertical segments">
                    <div class="ui center aligned inverted segment">
                        Player Name
                    </div>
                    <div id="firstName" class="ui center aligned segment">
                        MS
                    </div>
                </div>
            </div>
            <div class="ui segment">
                <div class="ui vertical segments">
                    <div class="ui center aligned inverted segment">
                        Total Score
                    </div>
                    <div id="firstScore" class="ui center aligned segment">
                        100
                    </div>
                </div>
            </div>
        </div>
        </div>
    </body>
</html>
"""

@webpage.route('/')
def home():
    return render_template_string(htmlCode)

if __name__ == '__main__':
    webpage.run(host=leaderboardip, port=int(leaderboardport))
