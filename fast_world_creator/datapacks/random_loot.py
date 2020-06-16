import io
import json
import logging
import os
import random
import shutil
from zipfile import ZipFile, ZIP_DEFLATED

from fast_world_creator.datapacks.base_datapack import Datapack
from fast_world_creator.utils import common_utils as cu


class RandomLootDataPack(Datapack):

    def __init__(self):
        super().__init__()
        self.name = "random_loot"
        self.description = "Loot table randomizer"
        self.default_enabled = False

    def _create_datapack_files(self, version: str, seed: int = None, *args,
                               **kwargs) -> bool:
        """ Create the necessary datapack files.

        :param version: The version of Minecraft to use as base (e.g. '1.15.2').
        :param seed: The seed to use for the randomization of the loot tables.
        :return: True if the files were created successfully.
        """
        self.datapack_files.append({
            "path": 'pack.mcmeta',
            "data": json.dumps(
                {
                    "pack": {
                        "pack_format": 5,
                        "description": f"{self.description}"
                    }
                },
                indent=4
            )
        })
        if not self._extract_loot_tables(version):
            return False
        self._add_loot_tables(seed)
        # Clean up extracted loot tables
        shutil.rmtree(f"{os.getcwd()}/data", ignore_errors=True)
        return True

    def _extract_loot_tables(self, version: str) -> bool:
        """ Extract the loot tables from a Minecraft client jar.

        :param version: The version of Minecraft to use as base (e.g. '1.15.2').
        :return: False if version is not installed
        """
        jar_path = cu.find_installed_minecraft_versions().get(version, None)
        if not jar_path:
            logging.error(f"{version} is not installed. Can't randomize loot.")
            return False
        logging.info(f"Extracting {version} loot tables")
        with ZipFile(jar_path) as jar_file:
            for item in jar_file.namelist():
                if item.startswith("data/minecraft/loot_tables"):
                    item_output = f"{os.getcwd()}/{item}"
                    os.makedirs(
                        os.sep.join(item_output.split("/")[:-1]),
                        exist_ok=True)
                    with open(item_output, "wb") as item_file:
                        item_file.write(jar_file.read(item))
        return True

    def _add_loot_tables(self, seed: int = None) -> None:
        """ Randomize the loot tables contents and add them to this datapack.

        The file paths are stored into two lists and one of the lists is
        randomized using the provided seed. Then, the contents of the path in
        one list are stored in the path of the other list. This ensures that
        there are no mismatches between the amount of files.

        However, not every single datapack file will contain correct contents
        for the loot table it represents. Minecraft takes care of invalid loot
        tables and logs warnings in the console upon launch.

        :param seed: The seed to use for randomization of the loot tables.
        """
        lt_files = []
        for dirpath, dirnames, filenames in os.walk("data"):
            for filename in filenames:
                lt_files.append(f"{dirpath}/{filename}")
        lt_file_contents = lt_files.copy()
        logging.info(
            f"Randomizing {len(lt_files)} loot tables with seed = {seed}")
        random.seed(seed)
        random.shuffle(lt_file_contents)
        for lt_file, lt_content in zip(lt_files, lt_file_contents):
            with open(lt_content) as file_content:
                lt_data = file_content.read()
                self.datapack_files.append({
                    "path": lt_file,
                    "data": lt_data
                })

    def store(self) -> None:
        """ Store the datapack as a zip file. """
        zip_bytes = io.BytesIO()
        with ZipFile(zip_bytes, 'w', ZIP_DEFLATED, False) as zip_f:
            for file in self.datapack_files:
                zip_f.writestr(
                    zinfo_or_arcname=file["path"],
                    data=file["data"]
                )
        with open(f"datapacks/{self.name}.zip", 'wb') as file:
            file.write(zip_bytes.getvalue())
