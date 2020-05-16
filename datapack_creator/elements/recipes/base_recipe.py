class RecipeBase:

    recipe_type = None
    group = None
    result = None

    def __init__(self):
        super().__init__()

    def get_path(self) -> str:
        return "/.json"

    def to_data(self):
        pass
