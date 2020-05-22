import os
from typing import List, Union

from fast_world_creator.datapacks.random_loot import RandomLootDataPack
from fast_world_creator.datapacks.external_datapack import ExternalDatapack


def get_available_datapacks() -> List[
        Union[RandomLootDataPack, ExternalDatapack]]:
    datapacks = [RandomLootDataPack()]
    external_datapack_folder = f"{os.getcwd()}/assets/imported_datapacks"
    for z in os.listdir(external_datapack_folder):
        if z.endswith(".zip"):
            dp = ExternalDatapack(f"{external_datapack_folder}/{z}")
            datapacks.append(dp)
    return datapacks
