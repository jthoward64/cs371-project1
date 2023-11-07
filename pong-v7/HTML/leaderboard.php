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
                </div>
            </div>
            <div class="ui segment">
                <div id="scoreHolder" class="ui vertical segments">
                    <div id='scoreHeader' class="ui center aligned inverted segment">
                        Total Wins
                    </div>
                </div>
            </div>
        </div>
        </div>
    </body>
    <script>
        // The refresh button used to grab the leaderboard from the server
        const refreshButton = document.getElementById('refreshButton');

        // The URL of our server
        const dataPath = 'http://localhost:8500/leaderboard';

        // Holds our leaderboard
        const scoreHolder = document.getElementById('scoreHolder');
        const nameHolder = document.getElementById('nameHolder');

        // Grabs our new leaderboard data, manipulates the leaderboard
        function loadboard() {
            // Grab new data
            fetch(dataPath)
            .then(response => {
                if (!response.ok) { // Check if response came back fine
                    throw new Error('Network error ' + response.statusText);
                }
                return response.json(); // Parse JSON data
            })
            .then(data => {
                // Check if data is actually present
                if (!data) {
                    throw new Error('Data is null or undefined');
                }

                // Clear the leaderboard
                scoreHolder.innerHTML = "<div class='ui center aligned inverted segment'>Total Score</div>";
                nameHolder.innerHTML = "<div class='ui center aligned inverted segment'>Player Name</div>";

                // Check if data is an object
                if (typeof data === 'object' && data !== null) {
                    // Iterate over object and add entries to leaderboard
                    for (const [initial, score] of Object.entries(data)) {
                        const newName = `<div class='ui center aligned segment'>${initial}</div>`;
                        const newScore = `<div class='ui center aligned segment'>${score}</div>`;

                        scoreHolder.innerHTML += newScore;
                        nameHolder.innerHTML += newName;
                    }
                } else {
                    console.error('Unexpected data type:', data);
                }
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
        }

        // When the client clicks "Refresh", refresh the leaderboard.
        refreshButton.addEventListener('click', loadboard);

        // Load the leaderboard when the page is ready
        window.addEventListener('load', loadboard);
    </script>
</html>