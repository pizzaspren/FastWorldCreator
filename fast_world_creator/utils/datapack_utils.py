import os
import shutil
import zipfile
from typing import List, Type, Union

from datapack_creator.elements.datapacks.base_datapack import Datapack
from fast_world_creator.datapacks import RandomLootDataPack
from fast_world_creator.datapacks.external_datapack import ExternalDatapack
from fast_world_creator.utils import common_utils as cu


def extract_loot_tables(jar_path: str) -> None:
    """ Extracts the folder 'data/minecraft/loot_tables' from the jar. """
    cu.log(f"Extracting {os.path.split(jar_path)[-1]} loot tables")
    with zipfile.ZipFile(jar_path) as jar_file:
        for item in jar_file.namelist():
            if item.startswith("data/minecraft/loot_tables"):
                item_output = os.sep.join([
                    os.getcwd(),
                    item.lstrip("data/minecraft/")
                ]).replace("/", os.sep)
                os.makedirs(
                    os.sep.join(item_output.split(os.sep)[:-1]),
                    exist_ok=True)
                with open(item_output, "wb") as item_file:
                    item_file.write(jar_file.read(item))


def delete_loot_tables() -> None:
    shutil.rmtree(
        os.sep.join([os.getcwd(), "loot_tables"]),
        ignore_errors=True
    )


def get_available_datapacks() -> List[Union[str, Type[Datapack]]]:
    datapacks = [
        RandomLootDataPack
    ]
    external_datapack_folder = f"{os.getcwd()}/assets/imported_datapacks"
    for z in os.listdir(external_datapack_folder):
        if z.endswith(".zip"):
            dp = ExternalDatapack(f"{external_datapack_folder}/{z}")
            datapacks.append(dp)
    return datapacks
