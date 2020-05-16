from datapack_creator.elements.recipes.base_cooking_recipe import \
    CookingRecipeBase


class SmeltingRecipe(CookingRecipeBase):

    def __init__(self, name, ingredient, output, xp=0.1, time=200, group=None):
        super().__init__(name, ingredient, output, xp, time, group)
        self.recipe_type = "minecraft:smelting"
