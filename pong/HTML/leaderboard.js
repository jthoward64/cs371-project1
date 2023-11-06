// The refresh button used to grab the leaderboard from the server
const refreshButton = document.getElementById("refreshButton");

// The URL of our server
const DATA_URL = "localhost:6000";

// Holds our leaderboard
const scoreHolder = document.getElementById("scoreHolder");
const nameHolder = document.getElementById("nameHolder");

// The format of the header element in each section
const scoreHeader =
  "<div class='ui center aligned inverted segment'>Total Score</div>";
const nameHeader =
  "<div class='ui center aligned inverted segment'>Player Name</div>";

// Grabs our new leaderboard data, manipulates the leaderboard
async function loadBoard() {
  // Grab new data
  const response = await fetch(DATA_URL);
  if (!response.ok) {
    console.error("Error fetching data: " + response.statusText, response);
    throw new Error(response.statusText);
  }
  const data = await response.json();
  console.log("Data Received: ", data);

  // Clear the leaderboard
  scoreHolder.innerHTML = "";
  nameHolder.innerHTML = "";

  // Loop through the leaderboard data and load it
  // this code is not quite right, score is the index of the array, not the score
  data.numberList.forEach((initial, score) => {
    // Get the corresponding button by its ID
    const newName = `<div class='ui center aligned segment'>${initial}</div>`;
    const newScore = `<div class='ui center aligned segment'>${score}</div>`;

    scoreHolder.innerHTML += newScore;
    nameHolder.innerHTML += newName;
  });
}

// When the client clicks "Refresh", refresh the leaderboard.
refreshButton.addEventListener("click", () => loadBoard().catch(console.error));

// When the client first joins, load the leaderboard page.
loadBoard().catch(console.error);
