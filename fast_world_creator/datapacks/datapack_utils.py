import json
import os
import shutil
import zipfile
from typing import List, Type, Union

from fast_world_creator.datapacks.convenient_crafting import \
    ConvenientCraftingDataPack
from fast_world_creator.datapacks.datapack_base import Datapack
from fast_world_creator.datapacks.external_datapack import ExternalDatapack
from fast_world_creator.datapacks.more_advancements import \
    MoreAdvancementsDataPack
from fast_world_creator.datapacks.random_loot import RandomLootDataPack
from fast_world_creator.utils import common_utils as cu


def create_shaped_crafting_recipe(pattern, key, result, result_amount=1):
    return json.dumps({
        "type": "minecraft:crafting_shaped",
        "pattern": pattern,
        "key": key,
        "result": {
            "item": result,
            "count": result_amount
        }
    })


def create_shapeless_crafting_recipe(items, result, result_amount=1):
    return json.dumps({
        "type": "minecraft:crafting_shapeless",
        "ingredients": [dict(item=i) for i in items],
        "result": {
            "item": result,
            "count": result_amount
        }
    })


def create_furnace_recipe(recipe_type, items, result, xp, cooking_time):
    return json.dumps({
        "type": recipe_type,
        "ingredient": [dict(item=i) for i in items],
        "result": result,
        "experience": xp,
        "cookingtime": cooking_time
    })


def create_smelting_recipe(items, result, xp=0.1, cooking_time=200):
    return create_furnace_recipe("minecraft:smelting",
                                 items, result, xp, cooking_time)


def create_smoking_recipe(items, result, xp=0.1, cooking_time=100):
    return create_furnace_recipe("minecraft:smoking",
                                 items, result, xp, cooking_time)


def create_blasting_recipe(items, result, xp=0.1, cooking_time=100):
    return create_furnace_recipe("minecraft:blasting",
                                 items, result, xp, cooking_time)


def extract_loot_tables(jar_path: str):
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


def delete_loot_tables():
    shutil.rmtree(
        os.sep.join([os.getcwd(), "loot_tables"]),
        ignore_errors=True
    )


def get_available_datapacks() -> List[Union[str, Type[Datapack]]]:
    datapacks = [
        RandomLootDataPack,
        ConvenientCraftingDataPack,
        MoreAdvancementsDataPack
    ]
    external_datapack_folder = f"{os.getcwd()}/assets/imported_datapacks"
    for z in os.listdir(external_datapack_folder):
        if z.endswith(".zip"):
            dp = ExternalDatapack(f"{external_datapack_folder}/{z}")
            datapacks.append(dp)
    return datapacks
