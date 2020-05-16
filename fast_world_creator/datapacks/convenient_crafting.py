from datapack_creator.elements.datapacks.base_datapack import Datapack
from datapack_creator.elements.item import Item
from datapack_creator.elements.recipes import *
from datapack_creator.elements.tag import Tag


class ConvenientCraftingDataPack(Datapack):
    name = "convenient_crafting"
    description = "Convenient and balanced crafting recipes"

    def __init__(self):
        super().__init__()

    def _shaped_recipes(self):
        iron_ingot = Item("minecraft:iron_ingot")
        coals = Tag("minecraft:coals")

        self.add_element(ShapedCraftingRecipe(
            "iron_ingot",
            [
                "III",
                "ICI",
                "III"
            ],
            {
                "I": Item("minecraft:iron_ore").as_ingredient(),
                "C": coals.to_ingredient()
            },
            iron_ingot, 8
        ))
        self.add_element(ShapedCraftingRecipe(
            "gold_ingot",
            [
                "III",
                "ICI",
                "III"
            ],
            {
                "I": Item("minecraft:gold_ore").as_ingredient(),
                "C": coals.to_ingredient()
            },
            Item("minecraft:gold_ingot"), 8
        ))
        self.add_element(ShapedCraftingRecipe(
            "diamond", [
                "III",
                "ICI",
                "III"
            ],
            {
                "I": Item("minecraft:diamond_ore").as_ingredient(),
                "C": coals.to_ingredient()
            },
            Item("minecraft:diamond"), 8
        ))
        self.add_element(ShapedCraftingRecipe(
            "quartz2",
            [
                "III",
                "ICI",
                "III"
            ],
            {
                "I": Item("minecraft:nether_quartz_ore").as_ingredient(),
                "C": coals.to_ingredient()
            },
            Item("minecraft:quartz"), 8
        ))
        self.add_element(ShapedCraftingRecipe(
            "lapis_lazuli",
            [
                "III",
                "ICI",
                "III"
            ],
            {
                "I": Item("minecraft:lapis_ore").as_ingredient(),
                "C": coals.to_ingredient()
            },
            Item("minecraft:lapis_lazuli"), 8
        ))
        self.add_element(ShapedCraftingRecipe(
            "redstone",
            [
                "III",
                "ICI",
                "III"
            ],
            {
                "I": Item("minecraft:redstone_ore").as_ingredient(),
                "C": coals.to_ingredient()
            },
            Item("minecraft:redstone"), 8
        ))
        self.add_element(ShapedCraftingRecipe(
            "charcoal",
            [
                "III",
                "ICI",
                "III"
            ],
            {
                "I": Tag("minecraft:logs_that_burn").to_ingredient(),
                "C": coals.to_ingredient()
            },
            Item("minecraft:charcoal"), 8
        ))
        self.add_element(ShapedCraftingRecipe(
            "chest_minecart",
            [
                "ICI",
                "III"
            ],
            {
                "I": iron_ingot.as_ingredient(),
                "C": Item("minecraft:chest").as_ingredient()
            },
            Item("minecraft:chest_minecart"), 1
        ))
        self.add_element(ShapedCraftingRecipe(
            "furnace_minecart",
            [
                "ICI",
                "III"
            ],
            {
                "I": iron_ingot.as_ingredient(),
                "C": Item("minecraft:furnace").as_ingredient()
            },
            Item("minecraft:furnace_minecart"), 1
        ))
        self.add_element(ShapedCraftingRecipe(
            "hopper_minecart",
            [
                "ICI",
                "III"
            ],
            {
                "I": iron_ingot.as_ingredient(),
                "C": Item("minecraft:hopper").as_ingredient()
            },
            Item("minecraft:hopper_minecart"), 1
        ))
        self.add_element(ShapedCraftingRecipe(
            "tnt_minecart",
            [
                "ICI",
                "III"
            ],
            {
                "I": iron_ingot.as_ingredient(),
                "C": Item("minecraft:tnt").as_ingredient()
            },
            Item("minecraft:tnt_minecart"), 1
        ))
        self.add_element(ShapedCraftingRecipe(
            "enchanted_golden_apple",
            [
                "GGG",
                "GAG",
                "GGG"
            ],
            {
                "G": Item("minecraft:gold_block").as_ingredient(),
                "A": Item("minecraft:apple").as_ingredient()
            },
            Item("minecraft:enchanted_golden_apple"), 1
        ))
        self.add_element(ShapedCraftingRecipe(
            "saddle",
            [
                "LLL",
                "HLH"
            ],
            {
                "L": Item("minecraft:leather").as_ingredient(),
                "H": Item("minecraft:tripwire_hook").as_ingredient()
            },
            Item("minecraft:saddle"), 1
        ))
        self.add_element(ShapedCraftingRecipe(
            "white_wool",
            [
                "WWW",
                "WDW",
                "WWW"
            ],
            {
                "D": Item("minecraft:white_dye").as_ingredient(),
                "W": Tag("minecraft:wool").to_ingredient()
            },
            Item("minecraft:white_wool"), 8
        ))
        self.add_element(ShapedCraftingRecipe(
            "grass_block",
            [
                "G",
                "D"
            ],
            {
                "G": Item("minecraft:grass").as_ingredient(),
                "D": Item("minecraft:dirt").as_ingredient()
            },
            Item("minecraft:grass_block"), 1
        ))
        self.add_element(ShapedCraftingRecipe(
            "snow_block",
            [
                "SS",
                "SS"
            ],
            {
                "S": Item("minecraft:snow").as_ingredient()
            },
            Item("minecraft:snow_block"), 1
        ))

    def _shapeless_recipes(self):
        self.add_element(ShapelessCraftingRecipe(
            "book",
            Item("minecraft:leather") * 1 + Item("minecraft:sugar_cane") * 3,
            Item("minecraft:book"), 1
        ))
        self.add_element(ShapelessCraftingRecipe(
            "bone_block",
            Item("minecraft:bone") * 3,
            Item("minecraft:bone_block"), 1
        ))
        self.add_element(ShapelessCraftingRecipe(
            "clay_ball",
            Item("minecraft:clay") * 1,
            Item("minecraft:clay_ball"), 4
        ))
        self.add_element(ShapelessCraftingRecipe(
            "honeycomb",
            Item("minecraft:honeycomb_block") * 1,
            Item("minecraft:honeycomb"), 4
        ))
        self.add_element(ShapelessCraftingRecipe(
            "brick",
            Item("minecraft:bricks") * 1,
            Item("minecraft:brick"), 4
        ))
        self.add_element(ShapelessCraftingRecipe(
            "quartz",
            Item("minecraft:quartz_block") * 1,
            Item("minecraft:quartz"), 4
        ))
        self.add_element(ShapelessCraftingRecipe(
            "glass",
            Item("minecraft:glowstone") * 1,
            Item("minecraft:glowstone_dust"), 4
        ))
        self.add_element(ShapelessCraftingRecipe(
            "flint",
            Item("minecraft:gravel") * 1,
            Item("minecraft:flint"), 1
        ))
        self.add_element(ShapelessCraftingRecipe(
            "name_tag",
            Item("minecraft:lead") * 1 + Item("minecraft:paper") * 1,
            Item("minecraft:name_tag"), 1
        ))
        self.add_element(ShapelessCraftingRecipe(
            "string",
            Item("minecraft:white_wool") * 1,
            Item("minecraft:string"), 4
        ))
        self.add_element(ShapelessCraftingRecipe(
            "ice",
            Item("minecraft:packed_ice") * 1,
            Item("minecraft:ice"), 9
        ))
        self.add_element(ShapelessCraftingRecipe(
            "packed_ice",
            Item("minecraft:blue_ice") * 1,
            Item("minecraft:packed_ice"), 9
        ))

        self.add_element(ShapelessCraftingRecipe(
            "coalblock",
            Item("minecraft:charcoal") * 9,
            Item("minecraft:coal_block"), 1
        ))

    def _smoking_recipes(self):
        self.add_element(SmokingRecipe(
            "smoking_leather",
            Item("minecraft:rotten_flesh").as_ingredient(),
            Item("minecraft:leather")
        ))
