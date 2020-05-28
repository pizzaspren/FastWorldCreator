class Datapack:

    def __init__(self):
        super(Datapack, self).__init__()
        self.name = str()
        self.description = str()
        self.datapack_files = list()
        self.default_enabled = True

    def create_datapack_files(self, *args, **kwargs) -> None:
        """ Create the necessary files and store the datapack as a file. """
        self._create_datapack_files(*args, **kwargs)
        self.store()

    def _create_datapack_files(self, *args, **kwargs) -> None:
        """ Abstract method to create the necessary datapack files. """
        pass

    def store(self) -> None:
        """ Abstract method to store the datapack as a zip file. """
        pass
