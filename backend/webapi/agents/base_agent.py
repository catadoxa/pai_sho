from webapi.game import Game
import webapi.game_constants as constants


class BaseAgent(object):

    def __init__(self, game: Game):
        self.game = game

    def get_available_moves(self):
        pass

    def get_moves(self, piece):
        current_space = self.game.board.find_space(piece.x, piece.y)
        x, y = current_space.x, current_space.y
        moves = []
        for move in self.game.move_matrix:
            space = self.game.board.find_space(x + move.x, y + move.y)
            if space is not None:
                if not space.has_piece:
                    if piece.element != constants.Elements.LOTUS:
                        pass
                else:
                    pass

    def get_selectable_pieces(self):
        pass

    def choose_move(self):
        pass

    def next_player_number(self):
        return 1 - self.game.player_moving



