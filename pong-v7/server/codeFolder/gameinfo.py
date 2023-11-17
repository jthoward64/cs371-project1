import threading as th

class GameInfo:
    def __init__(self) -> None:
        self.game_lock = th.Lock()
        self.game_data = {
            'left': {
                'x': 0,
                'y': 0,
                'moving': '',
            },
            'right': {
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

        # Lock for basic game data
        self.basic_lock = th.Lock()

        # Is the game running
        self.game_running = False

        # Are the clients ready?
        self.ready = {
            'left': False,
            'right': False,
        }

        # Initials of the Players
        self.user = {
            'left': '',
            'right': ''
        }

        # Win Counter
        self.wins = {
            'left': 0,
            'right': 0
        }

    def grab_game(self, player:str) -> dict:
        '''Returns the current game data'''
        with self.game_lock:

            new_info = {
                'paddle': self.game_data[player],
                'ball': self.game_data['ball'],
                'score': self.game_data['score'],
                'sync': self.game_data['sync']
            }

            return new_info
    
    def update_game(self, player:str, data:dict) -> None:
        '''Updates the game data'''
        with self.game_lock:

            if data['sync'] > self.game_data['sync']:
                self.game_data['sync'] = data['sync']
                self.game_data['score'] = data['score']
                self.game_data['ball'] = data['ball']

            self.game_data[player] = data['paddle']

    def start_game(self, player:str) -> bool:
        '''Starts the Game Sequence'''
        with self.basic_lock:
            self.ready[player] = True
            self.game_running = self.ready['left'] and self.ready['right']
            return self.game_running
        
    def reset_start(self) -> None:
        '''Resets the Start Sequence'''
        with self.basic_lock:
            self.ready = {
                'left': False,
                'right': False,
            }

    def reset_game(self) -> None:
        with self.game_lock and self.basic_lock:
            self.game_data = {
                'left': {
                    'x': 0,
                    'y': 0,
                    'moving': '',
                },
                'right': {
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

            self.game_running = False

    def set_player(self, user:str) -> str:
        with self.basic_lock:
            if self.user['left'] == '':
                self.user['left'] = user
                return 'left'
            if self.user['right'] == '':
                self.user['right'] = user
                return 'right'
            
            return 'spectate'
        
    def increment_win(self, player:str):
        '''Increments the Wins in a Player'''
        with self.basic_lock:
            self.wins[player] += 1