import logging


class Datapack:

    def __init__(self):
        super(Datapack, self).__init__()
        self.name = str()
        self.description = str()
        self.datapack_files = list()
        self.default_enabled = True

    def create_datapack_files(self, *args, **kwargs) -> bool:
        """ Create the necessary files and store the datapack as a file. """
        logging.info(f"Creating files for datapack '{self.name}'")
        if self._create_datapack_files(*args, **kwargs):
            logging.info(f"Storing files for datapack '{self.name}'")
            self.store()
            return True

    def _create_datapack_files(self, *args, **kwargs) -> bool:
        """ Abstract method to create the necessary datapack files. """
        return True

    def store(self) -> None:
        """ Abstract method to store the datapack as a zip file. """
