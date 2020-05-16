from datapack_creator.elements.recipes.base_recipe import RecipeBase


class ShapelessCraftingRecipe(RecipeBase):

    def __init__(self, name, ingredients, output, count=1, group=None):
        super().__init__(name, output, group)
        self.recipe_type = "minecraft:crafting_shapeless"
        self.ingredients = ingredients
        self.output_count = count

    def _update_data_dict(self, data_dict: dict):
        data_dict.update({
            "ingredients": [dict(item=i) for i in self.ingredients],
            "result": {
                "item": self.output,
                "count": self.output_count
            }
        })
