import os
from typing import List, Union

from fast_world_creator.datapacks.external_datapack import ExternalDatapack
from fast_world_creator.datapacks.random_loot import RandomLootDataPack


def get_available_datapacks() -> List[
        Union[RandomLootDataPack, ExternalDatapack]]:
    """ Get a list of the datapacks that can be added to a world.

    Reads the zip files available in the assets/imported_datapacks folder and
    creates an ExternalDatapack object with their path and name. The external
    datapacks are then appended after a RandomLootDatapack object, which is
    built during program runtime.

    :return: A list of the available datapacks.
    """
    datapacks = [RandomLootDataPack()]
    external_datapack_folder = f"{os.getcwd()}/assets/imported_datapacks"
    for z in os.listdir(external_datapack_folder):
        if z.endswith(".zip"):
            dp = ExternalDatapack(f"{external_datapack_folder}/{z}")
            datapacks.append(dp)
    return datapacks
