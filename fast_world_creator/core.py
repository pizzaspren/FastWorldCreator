import random

from fast_world_creator.new_world import world_creator
from fast_world_creator.utils import common_utils as cu


def run(version_pair, world_name, seed, datapacks, gamerules,
        difficulty=2, game_mode=0, generator="default", generator_options=None,
        raining=False, thundering=False):
    wc = world_creator.WorldCreator(
        mc_release=version_pair[0],
        world_name=world_name or f"FastNewWorld_{random.randint(0, 1000000)}",
        seed=seed
    )
    owd = cu.change_directory(wc.create_world_directory())
    if datapacks:
        wc.create_datapack_directory()
        for d in datapacks:
            d().create_datapack_files(seed=wc.seed, jar_path=version_pair[1])
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
