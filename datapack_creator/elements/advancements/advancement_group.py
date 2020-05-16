class AdvancementGroup:
    group = ""

    def __init__(self, group):
        self.group = group

    def __str__(self):
        return self.group

    def __repr__(self):
        return self.__str__()
