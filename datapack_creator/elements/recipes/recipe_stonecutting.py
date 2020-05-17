from .base_recipe import RecipeBase


class StonecuttingRecipe(RecipeBase):

    def __init__(self, name, ingredient, output, count=1, group=None):
        super().__init__(name, output, group)
        self.recipe_type = "minecraft:stonecutting"
        self.ingredient = ingredient
        self.count = count

    def _update_data_dict(self, data_dict):
        data_dict["ingredient"] = self.ingredient
        data_dict["count"] = self.count
