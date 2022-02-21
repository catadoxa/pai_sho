from enum import Enum


class EnumDict(Enum):
    @classmethod
    def as_dict(cls):
        return {name: member.value for name, member in cls.__members__.items()}

    @classmethod
    def as_list(cls):
        return [element.value.asdict() if cls.check_asdict(element.value, 'asdict') else element.value for element in cls]

    @staticmethod
    def check_asdict(item, attr):
        member = getattr(item, attr, False)
        return member and callable(member)


class Elements(EnumDict):
    FIRE = 'FIRE'
    AIR = 'AIR'
    WATER = 'WATER'
    EARTH = 'EARTH'
    LOTUS = 'LOTUS'
    AVATAR = 'AVATAR'


class TakeMatrix(EnumDict):
    FIRE = [Elements.AIR.name, Elements.AVATAR.name]
    AIR = [Elements.WATER.name, Elements.AVATAR.name]
    WATER = [Elements.EARTH.name, Elements.AVATAR.name]
    EARTH = [Elements.FIRE.name, Elements.AVATAR.name]
    LOTUS = []
    AVATAR = [Elements.AIR.name, Elements.WATER.name, Elements.EARTH.name, Elements.FIRE.name, Elements.AVATAR.name]


class Position(object):
    __slots__ = ['x', 'y']

    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    @classmethod
    def fromdict(cls, pos_dict):
        return cls(pos_dict['x'], pos_dict['y'])

    def asdict(self):
        return {'x': self.x, 'y': self.y}


class MoveMatrix(EnumDict):
    N = Position(0, 2)
    S = Position(0, -2)
    E = Position(2, 0)
    W = Position(-2, 0)
    NE = Position(1, 1)
    SE = Position(1, -1)
    SW = Position(-1, -1)
    NW = Position(-1, 1)






