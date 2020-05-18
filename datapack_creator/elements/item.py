class Item:

    def __init__(self, name, nbt=""):
        self.name = name
        self.nbt = nbt

    def as_ingredient(self):
        """To be used in shaped crafting recipes and advancements"""
        ingredient_dict = dict(item=self.name)
        if self.nbt:
            ingredient_dict["nbt"] = self.nbt
        return ingredient_dict

    def __mul__(self, other):
        """To be used in shapeless crafting recipes"""
        if isinstance(other, int):
            return [self.name] * other
        return self

    def __str__(self):
        return self.name
