from datapack_creator.elements.recipes.base_recipe import RecipeBase


class CookingRecipeBase(RecipeBase):

    def __init__(self, name, ingredient, output, xp=0.1, time=100, group=None):
        super().__init__(name, output, group)
        self.ingredient = ingredient
        self.xp = xp
        self.time = time

    def _update_data_dict(self, data_dict):
        data_dict["ingredient"] = self.ingredient
        if self.xp:
            data_dict["experience"] = self.xp
        if self.time:
            data_dict["time"] = self.time
