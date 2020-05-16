import os
import random
from typing import List

from fast_world_creator.utils import common_utils as cu
from fast_world_creator.utils import minecraft_utils as mu


class WorldCreator:

    def __init__(self, mc_version: str, world_name: str, seed: int = None):
        self.mc_version = mc_version
        self.name = world_name
        self.seed = seed if seed is not None else random.randint(0, 1000000)
        self.w_dir = os.sep.join([cu.get_mc_folder(), "saves", self.name])

    def create_world_directory(self) -> str:
        try:
            os.mkdir(self.w_dir)
            return self.w_dir
        except FileExistsError:
            cu.log(f"World \'{self.name}\' already exists. Aborting")
            exit(-1)

    def create_datapack_directory(self) -> None:
        os.mkdir(os.sep.join([self.w_dir, "datapacks"]))

    def create_level_dat(self, datapack_list: List[str], difficulty: int = 2) -> None:
        """ Creates the level.dat NBT file in the new world folder. """
        from fast_world_creator.new_world.level_dat import LevelFile
        world_level_dat = os.sep.join([self.w_dir, "level.dat"])
        level_file = LevelFile.from_arguments({
            "arg_version": self.mc_version,
            "arg_world_name": self.name,
            "arg_seed": str(self.seed),
            "datapack_list": ",".join([f"{d}.zip" for d in datapack_list]),
            "arg_hardcore": str(int(mu.Difficulties(difficulty).is_hardcore())),
            "arg_diff": str(min(difficulty, 3))
        })
        level_file.save(filename=world_level_dat)
