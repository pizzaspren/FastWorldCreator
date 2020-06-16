import hashlib as hl
import logging
import os
import random
from typing import List

from fast_world_creator.new_world.level_dat import LevelFile
from fast_world_creator.utils import common_utils as cu
from fast_world_creator.utils import minecraft_utils as mu


class WorldCreator:

    def __init__(self, mc_release: str, world_name: str, seed: int = None):
        self.mc_release = mc_release
        self.name = world_name
        if not seed:
            logging.info("Seed was empty. Creating randomized seed.")
            seed = random.randint(0, 1000000)
        try:
            # Try to parse integer
            self.seed = int(seed)
        except ValueError:
            # No parsable integer. Create hash and convert lowest values to int
            self.seed = int(hl.md5(seed.encode("utf-8")).hexdigest()[:7], 16)
        logging.info(f"Seed = {self.seed}")
        self.w_dir = f"{cu.MC_FOLDER}/saves/{self.name}"

    def create_world_directory(self) -> str:
        """ Create the world folder based on the world name.

        Creates a world folder to store the new world. The name of the world
        folder will match the world name, except if the folder already exists.
        In that case, try to create a folder with the world seed appended.
        :return: The path to the created directory """
        try:
            if os.path.isdir(self.w_dir):
                self.w_dir += str(self.seed)
            logging.info(f"Creating world folder {self.w_dir}")
            os.mkdir(self.w_dir)
            return self.w_dir
        except FileExistsError as e:
            logging.error(f"World folder \'{self.name}\' already exists")
            raise e

    def create_datapack_directory(self) -> None:
        """ Create the datapack directory used to store all the datapack zips.

        Creates a folder named 'datapacks' in the world directory. Will
        intentionally fail if the world directory has not been created yet.
        """
        logging.info(f"Creating world datapacks folder {self.w_dir}")
        os.mkdir(f"{self.w_dir}/datapacks")

    def create_level_dat(self, gamerules: dict, difficulty: int,
                         datapack_list: List[str], game_mode: int = 0,
                         raining: bool = False, thundering: bool = False,
                         border_settings: dict = None,
                         generator: str = "default",
                         generator_opts: dict = None) -> None:
        """ Creates the level.dat NBT file in the new world folder.

        :param gamerules: A dictionary containing all the game rules and their
            values for this world.
        :param difficulty: An integer representing the difficulty of the world.
        :param datapack_list: The list of datapack names to enable in the world.
        :param game_mode: An integer representing the game mode of the player.
        :param raining: A boolean value indicating whether rain should be
            enabled. Gets overridden if the parameter thundering is True.
        :param thundering: A boolean value indicating whether thunder should be
            enabled. Overrides the parameter raining if set to True
        :param border_settings: Dictionary containing all the options for the
            world border.
        :param generator: The name of the terrain generator to use in the world.
        :param generator_opts: A dictionary containing the options for the flat
            and buffet terrain generators. If the parameter generator is neither
            "buffet" nor "flat", this parameter is ignored.
        """
        world_level_dat = f"{self.w_dir}/level.dat"
        logging.info(f"Starting creation of level.dat in '{world_level_dat}'")
        mc = "minecraft:"
        level_dat_dict = {
            "Version": {
                "Id": mu.version_map.get(self.mc_release),
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
            "generatorName": generator.lower(),
            "GameRules": gamerules,
            "GameType": game_mode,
            "raining": True if thundering else raining,
            "thundering": thundering or False,
            "BorderCenterX": float(border_settings.get("x")),
            "BorderCenterZ": float(border_settings.get("z")),
            "BorderDamagePerBlock": float(border_settings.get("damage")),
            "BorderSafeZone": float(border_settings.get("safe_blocks")),
            "BorderSize": float(border_settings.get("size")),
            "BorderSizeLerpTarget": float(border_settings.get("size_target")),
            "BorderSizeLerpTime": int(
                float(border_settings.get("lerp_time")) * 600),
            "BorderWarningBlocks": float(border_settings.get("warn_blocks")),
            "BorderWarningTime": float(border_settings.get("warn_time"))
        }
        if generator == "buffet":
            logging.info("Adding buffet options")
            generator_options_dict = {
                "biome_source": {
                    "type": mc + generator_opts.get("buffet_biome_type"),
                    "options": {
                        "size": generator_opts.get('buffet_size'),
                        "biomes": [mc + biome for biome in
                                   generator_opts.get("buffet_biomes")]
                    }
                },
                "chunk_generator": {
                    "options": {
                        "default_block": mc + generator_opts.get(
                            "buffet_block"),
                        "default_fluid": mc + generator_opts.get("buffet_fluid")
                    },
                    "type": mc + generator_opts.get("buffet_chunk_type")
                }
            }
            level_dat_dict["generatorOptions"] = generator_options_dict
        elif generator == "flat":
            logging.info("Adding superflat options")
            generator_layers = []
            for layer in generator_opts.get("flat_layers"):
                generator_layers.append({
                    "block": mc + layer[1],
                    "height": str(layer[0])
                })
            logging.info(f"Added {len(generator_layers)} layers to the world")
            generator_options_dict = {
                "biome": mc + generator_opts.get("flat_biome"),
                "layers": generator_layers,
                "structures": generator_opts.get("flat_structures")
            }
            level_dat_dict["generatorOptions"] = generator_options_dict

        logging.info("Parsing NBT tags")
        level_file = LevelFile.from_arguments(level_dat_dict)
        logging.info("Creating level.dat file")
        level_file.save(filename=world_level_dat)
