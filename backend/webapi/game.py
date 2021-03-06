import webapi.game_constants as constants
from webapi.board import Board
from uuid import uuid4
from webapi.move import *


class Game(object):
    __slots__ = ['move_matrix',
                 'take_matrix',
                 'players',
                 'board',
                 'player_moving',
                 'turn_number',
                 'winner',
                 'moves',
                 'current_move',
                 'game_id',
                 'game_name']

    def __init__(self, players, game_id=uuid4()):
        self.move_matrix = constants.MoveMatrix
        self.take_matrix = constants.TakeMatrix
        self.players = players
        self.board = Board()
        self.player_moving = 1
        self.turn_number = 0
        self.winner = None
        self.moves = []
        self.current_move = None
        self.game_id = game_id
        self.game_name = None

    def asdict(self):
        return dict(
            move_matrix=self.move_matrix.as_list(),
            take_matrix=self.take_matrix.as_dict(),
            players=self.players,
            board=None if self.board is None else self.board.asdict(),
            player_moving=self.player_moving,
            turn_number=self.turn_number,
            winner=self.winner,
            moves=self.moves,
            current_move=self.current_move,
            game_id=self.game_id,
            game_name=self.game_name
        )

    @classmethod
    def fromdict(cls, game_dict):
        game = cls(game_dict['players'])
        game.board = Board.fromdict(game_dict['board'])
        game.player_moving = game_dict['player_moving']
        game.turn_number = game_dict['turn_number']
        game.winner = game_dict['winner']
        game.moves = [Move.fromdict(move) for move in game_dict['moves']]
        game.current_move = game_dict['current_move']
        # FIXME actually need to use game names and ids at some point
        game.game_id = None  # game_dict['game_id']
        game.game_name = None
        return game

