<!DOCTYPE html>
    <head>
        <title>Pong Leaderboard</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js"></script>
        <script scr="leaderboard.js"></script>
    </head>
    <body>
        <div class="ui segment">
            <h1 class="ui center aligned segment">Pong Leaderboard</h1>
            <button id='refreshButton' class="ui fluid primay button">
                <i class="redo icon"></i>Refresh
            </button>
        <div class="ui horizontal segments">
            <div class="ui segment">
                <div id="nameHolder" class="ui vertical segments">
                    <div id="nameHeader" class="ui center aligned inverted segment">
                        Player Name
                    </div>
                    <div class="ui center aligned segment">
                        MS
                    </div>
                </div>
            </div>
            <div class="ui segment">
                <div id="scoreHolder" class="ui vertical segments">
                    <div id='scoreHeader' class="ui center aligned inverted segment">
                        Total Wins
                    </div>
                    <div class="ui center aligned segment">
                        100
                    </div>
                </div>
            </div>
        </div>
        </div>
    </body>
</html>