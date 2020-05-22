class Datapack:

    def __init__(self):
        super(Datapack, self).__init__()
        self.name = str()
        self.description = str()
        self.datapack_files = list()
        self.default_enabled = True

    def __call__(self, *args, **kwargs):
        return self

    def create_datapack_files(self, *args, **kwargs):
        self._create_datapack_files(*args, **kwargs)
        self.store()

    def _create_datapack_files(self, *args, **kwargs):
        pass

    def store(self):
        pass
