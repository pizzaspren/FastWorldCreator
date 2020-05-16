import json

from datapack_creator.elements import ElementBase


class RecipeBase(ElementBase):

    def __init__(self, name, output, group=None):
        super().__init__()
        self.recipe_type = None
        self.name = name
        self.group = group
        self.output = str(output)

    def get_path(self) -> str:
        return f"data/{self.datapack_name}/recipes/{self.name}.json"

    def to_data(self):
        data_dict = {
            "type": self.recipe_type,
            "result": str(self.output)
        }
        if self.group:
            data_dict["group"] = str(self.group)
        self._update_data_dict(data_dict)
        return json.dumps(data_dict)

    def _update_data_dict(self, data_dict):
        pass

    def __str__(self):
        return f"{self.datapack_name}:{self.name}"
