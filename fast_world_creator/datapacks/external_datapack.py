import os
import shutil

from fast_world_creator.datapacks.base_datapack import Datapack


class ExternalDatapack(Datapack):

    def __init__(self, path):
        super().__init__()
        self.name = path.split("/")[-1].rstrip(".zip")
        self.path = path
        self.description = "Found in assets/imported_datapacks"

    def create_datapack_files(self, *args, **kwargs):
        return self.store()

    def store(self):
        shutil.copy(self.path, f"{os.getcwd()}/datapacks/")
