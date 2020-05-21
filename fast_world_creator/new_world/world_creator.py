import hashlib as hl
import os
import random
from typing import List

from fast_world_creator.utils import common_utils as cu
from fast_world_creator.utils import minecraft_utils as mu
from fast_world_creator.utils.version_mapping import version_map


class WorldCreator:

    def __init__(self, mc_release: str, world_name: str, seed: int = None):
        self.mc_release = mc_release
        self.name = world_name
        if not seed:
            # Empty seed, create random seed
            seed = random.randint(0, 1000000)
        try:
            # Try to parse integer
            self.seed = int(seed)
        except ValueError:
            # No parsable integer. Create hash and convert lowest values to int
            self.seed = int(hl.md5(seed.encode("utf-8")).hexdigest()[:7], 16)
        self.w_dir = os.sep.join([cu.get_mc_folder(), "saves", self.name])

    def create_world_directory(self) -> str:
        try:
            if os.path.isdir(self.w_dir):
                # Simple duplicate prevention by appending seed, can still fail
                self.w_dir += str(self.seed)
            os.mkdir(self.w_dir)
            return self.w_dir
        except FileExistsError:
            cu.log(f"World \'{self.name}\' already exists. Aborting")
            exit(-1)

    def create_datapack_directory(self) -> None:
        os.mkdir(os.sep.join([self.w_dir, "datapacks"]))

    def create_level_dat(self, gamerules: dict, difficulty: int,
                         datapack_list: List[str], game_mode: int = 0,
                         raining: bool = False,
                         thundering: bool = False) -> None:
        """ Creates the level.dat NBT file in the new world folder. """
        from fast_world_creator.new_world.level_dat import LevelFile
        world_level_dat = os.sep.join([self.w_dir, "level.dat"])
        level_file = LevelFile.from_arguments({
            "Version": {
                "Id": version_map.get(self.mc_release),
                "Name": self.mc_release
            },
            "LevelName": self.name,
            "RandomSeed": self.seed,
            "DataPacks": {
                "Enabled": [f"file/{d}.zip" for d in datapack_list],
                "Disabled": []
            },
            "Difficulty": min(difficulty, 3),
            "hardcore": int(mu.Difficulties(difficulty).is_hardcore()),
            "GameRules": gamerules,
            "GameType": game_mode,
            "raining": raining,
            "thundering": thundering
        })
        level_file.save(filename=world_level_dat)
