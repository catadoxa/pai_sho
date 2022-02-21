from enum import Enum
from webapi.piece import Piece
from webapi.game_constants import Position


class MoveStepTypes(Enum):
    SINGLE = 1
    JUMP = 2
    END_TURN = 3
    REGENERATE_AVATAR = 4


class MoveStep(object):
    __slots__ = ['move_type',
                 'step_number',
                 'takes',
                 'initial_position',
                 'final_position']

    def __init__(self, move_type, step_number, takes, initial_position, final_position):
        self.move_type = move_type
        self.step_number = step_number
        self.takes = takes
        self.initial_position = initial_position
        self.final_position = final_position

    @classmethod
    def fromdict(cls, step_dict):
        return cls(
            step_dict['move_type'],
            step_dict['step_number'],
            None if step_dict['takes'] is None else [Piece.fromdict(take) for take in step_dict['takes']],
            None if step_dict['initial_position'] is None else Position(**step_dict['initial_position']),
            None if step_dict['final_position'] is None else Position(**step_dict['final_position'])
        )

    def asdict(self):
        return {
            'move_type': self.move_type,
            'step_number': self.step_number,
            'takes': None if self.takes is None else [p.asdict() for p in self.takes],
            'initial_position': None if self.initial_position is None else self.initial_position.asdict(),
            'final_position': None if self.final_position is None else self.final_position.asdict()
        }


class Move(object):
    __slots__ = ['steps',
                 'total_steps',
                 'player_number',
                 'move_number',
                 'piece']

    def __init__(self, steps, total_steps, player_number, move_number, piece):
        self.steps = steps
        self.total_steps = total_steps
        self.player_number = player_number
        self.move_number = move_number
        self.piece = piece

    @classmethod
    def fromdict(cls, move_dict):
        return cls(
            [MoveStep.fromdict(step) for step in move_dict['steps']],
            move_dict['total_steps'],
            move_dict['player_number'],
            move_dict['move_number'],
            Piece.fromdict(move_dict['piece'])
        )

    def asdict(self):
        return {
            'steps': [ms.asdict() for ms in self.steps],
            'total_steps': self.total_steps,
            'player_number': self.player_number,
            'move_number': self.move_number,
            'piece': self.piece.asdict()
        }


