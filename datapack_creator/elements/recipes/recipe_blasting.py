from .base_cooking_recipe import CookingRecipeBase


class BlastingRecipe(CookingRecipeBase):

    def __init__(self, name, ingredient, output, xp=0.1, time=100, group=None):
        super().__init__(name, ingredient, output, xp, time, group)
        self.recipe_type = "minecraft:blasting"
