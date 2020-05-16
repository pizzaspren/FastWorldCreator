from datapack_creator.elements.recipes.base_recipe import RecipeBase


class ShapedCraftingRecipe(RecipeBase):

    def __init__(self, name, pattern, keys, output, count=1, group=None):
        super().__init__(name, output, group)
        self.recipe_type = "minecraft:crafting_shaped"
        self.pattern = pattern
        self.keys = keys
        self.output_count = count

    def _update_data_dict(self, data_dict: dict):
        data_dict.update({
            "pattern": self.pattern,
            "key": self.keys,
            "result": {
                "item": self.output,
                "count": self.output_count
            }
        })
