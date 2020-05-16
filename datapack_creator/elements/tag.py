class Tag:

    def __init__(self, name):
        self.name = name

    def as_ingredient(self):
        """To be used in shaped crafting recipes"""
        return dict(tag=self.name)

    def __mul__(self, other):
        """To be used in shapeless crafting recipes"""
        if type(other) == int:
            return [self.name] * other
        return self

    def __str__(self):
        return self.name
