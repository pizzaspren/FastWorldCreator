import enum
import logging
from typing import List, Dict


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

    def values(self):
        return [e for e in Difficulties.__members__]


class GameModes(enum.IntEnum):
    """ Representation of the game modes in Minecraft. """
    SURVIVAL = 0
    CREATIVE = 1
    ADVENTURE = 2
    SPECTATOR = 3


# Representation of the different terrain generators in Minecraft
generator_names = ["Default", "Flat", "Largebiomes", "Amplified", "Buffet",
                   "Debug_all_block_states", "Default_1_1"]

# Distribution of biomes for the Buffet terrain generator
buffet_types = ["Fixed", "Checkerboard", "Vanilla_layered", "The_end"]

# Distribution of terrain for the Buffet terrain generator.
buffet_chunk_gen = ["Surface", "Caves", "Floating_islands", "Flat", "Debug"]


def get_mc_definitions(resource: str) -> List[str]:
    """ Load Minecraft values from the assets folder.

    :param resource: The resource to load from disk.
    :return: The lines of the file assets/minecraft_definitions/<resource>,
        without the line breaks.
    """
    logging.info(f"Loading definitions for '{resource}'")
    with open(f"assets/minecraft_definitions/{resource}.txt", "r") as f:
        return [line.rstrip("\n") for line in f.readlines() if line]


# Mapping between a release name and its data version.
# For more information, visit https://minecraft.gamepedia.com/Data_version.
version_map: Dict[str, str] = {
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
