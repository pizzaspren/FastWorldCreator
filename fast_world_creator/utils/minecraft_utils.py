import enum
from typing import List


class Difficulties(enum.IntEnum):
    """ Representation of the difficulties in Minecraft. """
    PEACEFUL = 0
    EASY = 1
    NORMAL = 2
    HARD = 3
    HARDCORE = 4

    def is_hardcore(self) -> bool:
        """ Whether the selected difficulty is equal to HARDCORE

        :return: True if and only if the object equals Difficulties.HARDCORE
        """
        return self is self.HARDCORE


class GameModes(enum.IntEnum):
    """ Representation of the game modes in Minecraft. """
    SURVIVAL = 0
    CREATIVE = 1
    ADVENTURE = 2
    SPECTATOR = 3


class GeneratorNames(enum.Enum):
    """ Representation of the different terrain generators in Minecraft. """
    DEFAULT = "default"
    FLAT = "flat"
    LARGEBIOMES = "largebiomes"
    AMPLIFIED = "amplified"
    BUFFET = "buffet"
    DEBUG_ALL_BLOCK_STATES = "debug_all_block_states"
    DEFAULT_1_1 = "default_1_1"


class BuffetOpts:
    """ Available options for the Buffet terrain generator. """

    class BType(enum.Enum):
        """ Distribution of biomes for the Buffet terrain generator. """
        FIXED = "fixed"
        CHECKERBOARD = "checkerboard"
        VANILLA_LAYERED = "vanilla_layered"
        THE_END = "the_end"

    class BChunkGen(enum.Enum):
        """ Distribution of terrain for the Buffet terrain generator. """
        SURFACE = "surface"
        CAVES = "caves"
        FLOATING_ISLANDS = "floating_islands"
        SUPERFLAT = "flat"
        DEBUG = "debug"


def get_mc_definitions(resource: str) -> List[str]:
    """ Load Minecraft values from the assets folder.

    :param resource: The resource to load from disk.
    :return: The lines of the file assets/minecraft_definitions/<resource>,
        without the line breaks.
    """
    with open(f"assets/minecraft_definitions/{resource}.txt", "r") as f:
        return [line.rstrip("\n") for line in f.readlines() if line]


def get_version_map() -> dict:
    """ Get the mapping between a release name and its data version.

    For more information, visit https://minecraft.gamepedia.com/Data_version.
    :return: A map of all the full releases between 1.13 and 1.15.2 (inclusive)
        and their data versions.
    """
    return {
        "1.15.2": "2230",
        "1.15.1": "2227",
        "1.15": "2225",
        "1.14.4": "1976",
        "1.14.3": "1968",
        "1.14.2": "1963",
        "1.14.1": "1957",
        "1.14": "1952",
        "1.13.2": "1631",
        "1.13.1": "1628",
        "1.13": "1519",
    }
