import io
import json
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

    def _create_datapack_files(self, jar_path, seed, *args, **kwargs) -> None:
        # Add mcmeta
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
        self._extract_loot_tables(jar_path)
        self._add_loot_tables(seed)
        shutil.rmtree(f"{os.getcwd()}/data", ignore_errors=True)

    def _extract_loot_tables(self, jar_path):
        cu.log(f"Extracting {os.path.split(jar_path)[-1]} loot tables")
        with ZipFile(jar_path) as jar_file:
            for item in jar_file.namelist():
                if item.startswith("data/minecraft/loot_tables"):
                    item_output = f"{os.getcwd()}/{item}"
                    os.makedirs(
                        os.sep.join(item_output.split("/")[:-1]),
                        exist_ok=True)
                    with open(item_output, "wb") as item_file:
                        item_file.write(jar_file.read(item))

    def _add_loot_tables(self, seed: int = None) -> None:
        lt_files = []
        for dirpath, dirnames, filenames in os.walk("data"):
            for filename in filenames:
                lt_files.append(f"{dirpath}/{filename}")
        lt_file_contents = lt_files.copy()
        if seed is None:
            seed = random.randint(0, 1000000)
        random.seed(seed)
        random.shuffle(lt_file_contents)
        for lt_file, lt_content in zip(lt_files, lt_file_contents):
            with open(lt_content) as file_content:
                lt_data = file_content.read()
                self.datapack_files.append({
                    "path": lt_file,
                    "data": lt_data
                })

    def store(self):
        zip_bytes = io.BytesIO()
        with ZipFile(zip_bytes, 'w', ZIP_DEFLATED, False) as zip_f:
            for file in self.datapack_files:
                zip_f.writestr(
                    zinfo_or_arcname=file["path"],
                    data=file["data"]
                )
        with open(f"datapacks/{self.name}.zip", 'wb') as file:
            file.write(zip_bytes.getvalue())
