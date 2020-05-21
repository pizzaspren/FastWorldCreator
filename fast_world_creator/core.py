import random

from fast_world_creator.new_world import world_creator
from fast_world_creator.utils import common_utils as cu, datapack_utils as du


def run(version_pair, world_name, seed, datapacks, gamerules,
        difficulty=2, game_mode=0, raining=False, thundering=False):
    wc = world_creator.WorldCreator(
        mc_release=version_pair[0],
        world_name=world_name or f"FastNewWorld_{random.randint(0, 1000000)}",
        seed=seed
    )
    owd = cu.change_directory(wc.create_world_directory())
    wc.create_datapack_directory()
    if datapacks:
        if any([d.needs_loot_tables() for d in datapacks]):
            du.extract_loot_tables(version_pair[1])
        for d in datapacks:
            creation_ok = d().create_datapack_files(seed=seed)
            if not creation_ok:
                print(f"Failed creation of datapack {d}")
        du.delete_loot_tables()
    else:
        datapacks = ""
    wc.create_level_dat(
        datapack_list=[d.name for d in datapacks],
        difficulty=difficulty,
        gamerules=gamerules,
        game_mode=game_mode,
        raining=raining,
        thundering=thundering
    )
    cu.change_directory(owd)
