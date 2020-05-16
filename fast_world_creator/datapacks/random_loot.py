import os
import random

from datapack_creator.elements.datapacks.base_datapack import Datapack


class RandomLootDataPack(Datapack):
    name = "random_loot"
    description = "Loot table randomizer"

    def __init__(self):
        super().__init__()
        # Override minecraft files
        self.datapack_name = "minecraft"

    @staticmethod
    def needs_loot_tables():
        return True

    def _create_others(self, seed: int = None) -> None:
        self._add_loot_tables(seed)

    def _add_loot_tables(self, seed: int = None) -> None:
        lt_files = []
        for dirpath, dirnames, filenames in os.walk("loot_tables"):
            for filename in filenames:
                lt_files.append(os.sep.join([dirpath, filename]))
        lt_file_contents = lt_files.copy()
        if seed is None:
            seed = random.randint(0, 1000000)
        random.seed(seed)
        random.shuffle(lt_file_contents)
        for lt_file, lt_content in zip(lt_files, lt_file_contents):
            with open(lt_content) as file_content:
                lt_data = file_content.read()
                self.add_datapack_file(
                    path_in_dp=f"{lt_file}",
                    data=lt_data
                )
