import enum


class Difficulties(enum.IntEnum):
    PEACEFUL = 0
    EASY = 1
    NORMAL = 2
    HARD = 3
    HARDCORE = 4

    def is_hardcore(self):
        return self is self.HARDCORE


class GameModes(enum.IntEnum):
    SURVIVAL = 0
    CREATIVE = 1
    ADVENTURE = 2
    SPECTATOR = 3
