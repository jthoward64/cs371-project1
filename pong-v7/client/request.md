# Game (game.py):
## Type: join_game
Description: A request from the Client to validate their login and join into playing or spectating the game

Required Parameters: new_message[username], new_message[password], new_message[initials]

Success: `{'request': 'join_game', 'return':True, 'message':player}`

Failure: `{'request': 'join_game', 'return':False, 'message': message}`


Return Parameters:
Success: 'player' = 'spectate' or 'left_player' or 'right_player'
Failure: 'message' = 'Account does not exists' or 'Incorrect Password'

## Type: game_info
Description: A request from the Client to obtain information on game

Success:`{'request': 'game_info', 'return':True, 'message':message}`

Return Parameters:
`message = {
    'left_player':self.information.left_initial,
    'right_player':self.information.right_initial,
    'game_code':self.code
}`

## Type: start_game
Description: A request from the Client to start the game
Note: Keep calling this function until the return is True before beginning the game UI-Run

Success: `{'request': 'ready', 'return':start, 'message':message}`

Return Parameters:
return: True if we start, False if we are waiting to start

`message = {
    'left_player':self.information.left_initial,
    'right_player':self.information.right_initial,
    'game_code':self.code
}`

## Type: grab_game
Description: A request from Client to grab the game information.
Note: If return is False, the game is over and we are waiting to either Exit or Replay the game

Success: `{'request': 'grab_game', 'return':True, 'message':game_info}`

Failure: `{'request': 'grab_game', 'return':False, 'message':None}`

Return Parameters:

`'message': {
    # This is the opponent's paddle
    'paddle': {
        'x': 0,
        'y': 0,
        'moving': '',
        },
    'ball': {
        'x': 0,
        'y': 0,
        'xVel': 0,
        'yVel': 0,
    },
    'score': {
        'lScore': 0,
        'rScore': 0,
    },
    'sync': 0,
}
`

## Type: update_game
Description: A method to update the game on the current progress

Required Parameters:

`'message': {
    # This is the player's paddle
    'left_paddle': {
        'x': 0,
        'y': 0,
        'moving': '',
        },
    'right_paddle': {
        'x': 0,
        'y': 0,
        'moving': '',
        },
    'ball': {
        'x': 0,
        'y': 0,
        'xVel': 0,
        'yVel': 0,
    },
    'score': {
        'lScore': 0,
        'rScore': 0,
    },
    'sync': 0,
}
`
