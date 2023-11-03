
// The refresh button used to grab the leaderboard from the server
const refreshButton = document.getElementById('refreshButton');

// The URL of our server
const dataPath = 'localhost:6000';

// Holds our leaderboard
const scoreHolder = document.getElementById('scoreHolder');
const nameHolder = document.getElementById('nameHolder');

// The format of the header element in each section
const scoreHeader = "<div class='ui center aligned inverted segment'>Total Score</div>";
const nameHeader = "<div class='ui center aligned inverted segment'>Player Name</div>";

// Grabs our new leaderboard data, manipulates the leaderboard
function loadboard(){
        // Grab new data
        fetch(dataPath)
        .then(response => response.json())
        .then(data => {
            console.log('Data Received: ', data);

            // Clear the leaderboard
            scoreHolder.innerHTML = '';
            nameHolder.innerHTML = '';
            
            // Loop through the leaderboard data and load it
            data.numberList.forEach((initial, score) => {
                // Get the corresponding button by its ID
                const newName = `<div class='ui center aligned segment'>${initial}</div>`;
                const newScore = `<div class='ui center aligned segment'>${score}</div>`;

                scoreHolder.innerHTML += newScore;
                nameHolder.innerHTML += newName;
        });
    })
}

// When the client clicks "Refresh", refresh the leaderboard.
refreshButton.addEventListener('click', loadboard);

// When the client first joins, load the leaderboard page.
loadboard();