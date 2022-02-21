from webapi.game_constants import Elements


class Piece(object):
    __slots__ = ['x', 'y', 'player_number', 'element']

    def __init__(self, x, y, player_number, element):
        self.x = x
        self.y = y
        self.player_number = player_number
        self.element = element

    def asdict(self):
        return dict(
            x=self.x,
            y=self.y,
            player_number=self.player_number,
            element=self.element.value
        )

    @classmethod
    def fromdict(cls, piece_dict):
        return cls(
            piece_dict['x'],
            piece_dict['y'],
            piece_dict['player_number'],
            Elements(piece_dict['element'])
        )

