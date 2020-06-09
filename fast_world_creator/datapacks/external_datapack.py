import os
import shutil

from fast_world_creator.datapacks.base_datapack import Datapack


class ExternalDatapack(Datapack):

    def __init__(self, path):
        super().__init__()
        self.name = path.split("/")[-1].rstrip(".zip")
        self.path = path
        self.description = "Found in assets/datapacks"

    def store(self) -> None:
        """ Copy the existing datapack zip to the datapacks folder."""
        shutil.copy(self.path, f"{os.getcwd()}/datapacks/")
