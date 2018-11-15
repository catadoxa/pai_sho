from webapi.piece import Piece
from webapi.space import Space
from webapi.utilities.class_to_dictionaries import jsonize, slots_object_to_dictionary
from flask import json

class Board(object):
    __slots__ = ['spaces', 'pieces']

    def __init__(self, top_player_num=0, bottom_player_num=1):
        self.spaces = self.make_spaces()
        self.pieces = self.make_initial_pieces(top_player_num, bottom_player_num)

    def make_spaces(self):
        spaces = []
        for i in range(-12, 13):
            for j in range(-12, 13):
                if i * i + j * j <= 12.5 * 12.5 and (i + j) % 2 == 0:
                    spaces.append(Space(i, j))
        return spaces

    def add_pieces(self, pieces):
        for piece in pieces:
            space = self.find_space(piece.x, piece.y)
            if space is not None:
                space.has_piece = True
                space.piece = piece

    def find_space(self, x, y):
        pass

    def find_piece(self, x, y):
        pass

    def make_initial_pieces(self, top_player_num, bottom_player_num):
        pieces = [
            Piece(-6, -8, bottom_player_num, Piece.Fire),
            Piece(-4, -8, bottom_player_num, Piece.Water),
            Piece(-3, -7, bottom_player_num, Piece.Earth),
            Piece(-3, -9, bottom_player_num, Piece.Air),
            Piece(-2, -10, bottom_player_num, Piece.Fire),
            Piece(-1, -11, bottom_player_num, Piece.Earth),
            Piece(0, -12, bottom_player_num, Piece.Lotus),
            Piece(1, -11, bottom_player_num, Piece.Air),
            Piece(2, -10, bottom_player_num, Piece.Water),
            Piece(3, -9, bottom_player_num, Piece.Earth),
            Piece(3, -7, bottom_player_num, Piece.Air),
            Piece(4, -8, bottom_player_num, Piece.Fire),
            Piece(6, -8, bottom_player_num, Piece.Water),
            Piece(0, -8, bottom_player_num, Piece.Avatar),

            Piece(-6, 8, top_player_num, Piece.Water),
            Piece(-4, 8, top_player_num, Piece.Fire),
            Piece(-3, 7, top_player_num, Piece.Air),
            Piece(-3, 9, top_player_num, Piece.Earth),
            Piece(-2, 10, top_player_num, Piece.Water),
            Piece(-1, 11, top_player_num, Piece.Air),
            Piece(0, 12, top_player_num, Piece.Lotus),
            Piece(1, 11, top_player_num, Piece.Earth),
            Piece(2, 10, top_player_num, Piece.Fire),
            Piece(3, 9, top_player_num, Piece.Air),
            Piece(3, 7, top_player_num, Piece.Earth),
            Piece(4, 8, top_player_num, Piece.Water),
            Piece(6, 8, top_player_num, Piece.Fire),
            Piece(0, 8, top_player_num, Piece.Avatar),
        ]
        return pieces

    def serializable(self):
        # return slots_object_to_dictionary(self)
        return dict(
            spaces=[str(space) for space in self.spaces],
            pieces=[str(piece )for piece in self.pieces]
        )

    def __str__(self):
        return json.dumps(self.serializable())

