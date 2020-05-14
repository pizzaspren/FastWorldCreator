import os
import shutil

from fast_world_creator.datapacks.datapack_base import Datapack


class ExternalDatapack(Datapack):

    def __init__(self, path):
        super().__init__()
        self.name = path.split("/")[-1]
        self.path = path
        self.description = "Found in assets/imported_datapacks"

    def __call__(self, *args, **kwargs):
        return self

    def create_datapack_files(self, *args, **kwargs):
        return self.store()

    def store(self) -> bool:
        return shutil.copy(self.path, os.sep.join([os.getcwd(), "datapacks/"]))
