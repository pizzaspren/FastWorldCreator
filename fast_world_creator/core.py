import random
from typing import Tuple, List

from fast_world_creator.datapacks.base_datapack import Datapack
from fast_world_creator.new_world import world_creator
from fast_world_creator.utils import common_utils as cu


def run(version_pair: Tuple[str, str], world_name: str, seed: int,
        datapacks: List[Datapack], gamerules: dict, difficulty: int = 2,
        game_mode: int = 0, generator: str = "default",
        generator_options: dict = None, raining: bool = False,
        thundering: bool = False) -> None:
    """ Create a minecraft world with the specified parameters.

    :param version_pair: Tuple containing the version name (e.g. '1.15.2') and
        the path to the Minecraft .jar file
    :param world_name: The name of the world to create.
    :param seed: The seed to use for the Minecraft world and the randomization
        of the random_loot datapack.
    :param datapacks: List of datapacks to enable for the world.
    :param gamerules: Dictionary containing all the gamerules for the version
        and the values to apply.
    :param difficulty: Integer representing the difficulty of the world.
    :param game_mode: Integer representing the game mode of the player.
    :param generator: The identifier for the terrain generator.
    :param generator_options: A dictionary containing the sub-options available
        for the Buffet and Flat generator types.
    :param raining: Whether it should be raining in the world.
    :param thundering: Whether it should be thundering in the world. Overrides
        the raining parameter if set to True.
    """
    wc = world_creator.WorldCreator(
        mc_release=version_pair[0],
        world_name=world_name or f"FastNewWorld_{random.randint(0, 1000000)}",
        seed=seed
    )
    owd = cu.change_directory(wc.create_world_directory())
    if datapacks:
        wc.create_datapack_directory()
        for d in datapacks:
            d.create_datapack_files(seed=wc.seed, jar_path=version_pair[1])
    else:
        datapacks = ""
    wc.create_level_dat(
        datapack_list=[d.name for d in datapacks],
        difficulty=difficulty,
        gamerules=gamerules,
        game_mode=game_mode,
        generator=generator,
        generator_opts=generator_options,
        raining=raining,
        thundering=thundering
    )
    cu.change_directory(owd)
