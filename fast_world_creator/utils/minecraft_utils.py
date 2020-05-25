import enum
from typing import List


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


class GeneratorNames(enum.Enum):
    DEFAULT = "default"
    FLAT = "flat"
    LARGEBIOMES = "largebiomes"
    AMPLIFIED = "amplified"
    BUFFET = "buffet"
    DEBUG_ALL_BLOCK_STATES = "debug_all_block_states"
    DEFAULT_1_1 = "default_1_1"


class BuffetOpts:
    class BType(enum.Enum):
        FIXED = "fixed"
        CHECKERBOARD = "checkerboard"
        VANILLA_LAYERED = "vanilla_layered"
        THE_END = "the_end"

    class BChunkGen(enum.Enum):
        SURFACE = "surface"
        CAVES = "caves"
        FLOATING_ISLANDS = "floating_islands"
        SUPERFLAT = "flat"
        DEBUG = "debug"


def get_mc_definitions(resource: str) -> List[str]:
    with open(f"assets/minecraft_definitions/{resource}.txt", "r") as f:
        return [line.rstrip("\n") for line in f.readlines() if line]
