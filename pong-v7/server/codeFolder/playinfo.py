import threading as th

from typing import Tuple

from helpers.database import Database as db

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

        self.database = db()

        # Lock for basic game data
        self.basic_lock = th.Lock()

        # Is the game running
        self.game_running = False

        # Are the clients ready?
        self.ready = {
            'left': False,
            'right': False,
        }

        # Username of the Players
        self.user = {
            'left': '',
            'right': ''
        }

        # Initials of the Players
        self.initials = {
            'left': '',
            'right': ''
        }

        # Win Counter
        self.wins = {
            'left': 0,
            'right': 0
        }

    def grab_game(self) -> dict:
        '''Returns the current game data'''
        with self.game_lock:
            new_info = {
                'left_paddle': self.game_data['left'],
                'right_paddle': self.game_data['right'],
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

    def set_player(self, user:str, initials:str) -> str:
        with self.basic_lock:
            if self.user['left'] == '':
                self.user['left'] = user
                self.initials['left'] = initials
                return 'left_player'
            if self.user['right'] == '':
                self.user['right'] = user
                self.initials['right'] = initials
                return 'right_player'
            
            return 'spectate'
        
    def grab_players(self) -> Tuple[str, str]:
        with self.basic_lock:
            return self.initials['left'], self.initials['right']
        
    def continue_game(self) -> bool:
        with self.basic_lock:
            return self.game_running
        
    def player_check(self, user:str) -> bool:
        with self.basic_lock:
            return self.user['left'] == user or self.user['right'] == user
        
    def increment_win(self, player:str):
        '''Increments the Wins in a Player'''
        with self.basic_lock:
            username = self.user[player]
            self.wins[player] += 1

            success, message, wins_number = self.database.grab_wins(username)

            if not success:
                print(f'Error: unable to grab wins,', message)
                return
            
            wins_number += 1

            success, message = self.database.update_wins(username, wins_number)

            if not success:
                print('Error: unable to update wins: ', message)