from datapack_creator.elements.datapacks.base_datapack import Datapack
from fast_world_creator.utils import datapack_utils


class ConvenientCraftingDataPack(Datapack):

    name = "convenient_crafting"
    description = "Convenient and balanced crafting recipes"

    def __init__(self):
        super().__init__()

    def _shaped_recipes(self):
        self.add_recipe_file(
            name="iron_ingot",
            data=datapack_utils.create_shaped_crafting_recipe(
                [
                    "III",
                    "ICI",
                    "III"
                ],
                {
                    "I": {"item": "minecraft:iron_ore"},
                    "C": {"tag": "minecraft:coals"}
                },
                "minecraft:iron_ingot", 8
            )
        )
        self.add_recipe_file(
            name="gold_ingot",
            data=datapack_utils.create_shaped_crafting_recipe(
                [
                    "III",
                    "ICI",
                    "III"
                ],
                {
                    "I": {"item": "minecraft:gold_ore"},
                    "C": {"tag": "minecraft:coals"}
                },
                "minecraft:gold_ingot", 8
            )
        )
        self.add_recipe_file(
            name="diamond",
            data=datapack_utils.create_shaped_crafting_recipe(
                [
                    "III",
                    "ICI",
                    "III"
                ],
                {
                    "I": {"item": "minecraft:diamond_ore"},
                    "C": {"tag": "minecraft:coals"}
                },
                "minecraft:diamond", 8
            )
        )
        self.add_recipe_file(
            name="quartz2",
            data=datapack_utils.create_shaped_crafting_recipe(
                [
                    "III",
                    "ICI",
                    "III"
                ],
                {
                    "I": {"item": "minecraft:nether_quartz_ore"},
                    "C": {"tag": "minecraft:coals"}
                },
                "minecraft:quartz", 8
            )
        )
        self.add_recipe_file(
            name="lapis_lazuli",
            data=datapack_utils.create_shaped_crafting_recipe(
                [
                    "III",
                    "ICI",
                    "III"
                ],
                {
                    "I": {"item": "minecraft:lapis_ore"},
                    "C": {"tag": "minecraft:coals"}
                },
                "minecraft:lapis_lazuli", 8
            )
        )
        self.add_recipe_file(
            name="redstone",
            data=datapack_utils.create_shaped_crafting_recipe(
                [
                    "III",
                    "ICI",
                    "III"
                ],
                {
                    "I": {"item": "minecraft:redstone_ore"},
                    "C": {"tag": "minecraft:coals"}
                },
                "minecraft:redstone", 8
            )
        )
        self.add_recipe_file(
            name="coalblock",
            data=datapack_utils.create_shaped_crafting_recipe(
                [
                    "III",
                    "III",
                    "III"
                ],
                {
                    "I": {"item": "minecraft:charcoal"},
                },
                "minecraft:coal_block", 1
            )
        )
        self.add_recipe_file(
            name="charcoal",
            data=datapack_utils.create_shaped_crafting_recipe(
                [
                    "III",
                    "ICI",
                    "III"
                ],
                {
                    "I": {"tag": "minecraft:logs_that_burn‌"},
                    "C": {"tag": "minecraft:coals"}
                },
                "minecraft:charcoal", 8
            )
        )
        self.add_recipe_file(
            name="chest_minecart",
            data=datapack_utils.create_shaped_crafting_recipe(
                [
                    "ICI",
                    "III"
                ],
                {
                    "I": {"item": "minecraft:iron_ingot"},
                    "C": {"item": "minecraft:chest"}
                },
                "minecraft:chest_minecart", 1
            )
        )
        self.add_recipe_file(
            name="furnace_minecart",
            data=datapack_utils.create_shaped_crafting_recipe(
                [
                    "ICI",
                    "III"
                ],
                {
                    "I": {"item": "minecraft:iron_ingot"},
                    "C": {"item": "minecraft:furnace"}
                },
                "minecraft:furnace_minecart", 1
            )
        )
        self.add_recipe_file(
            name="hopper_minecart",
            data=datapack_utils.create_shaped_crafting_recipe(
                [
                    "ICI",
                    "III"
                ],
                {
                    "I": {"item": "minecraft:iron_ingot"},
                    "C": {"item": "minecraft:hopper"}
                },
                "minecraft:hopper_minecart", 1
            )
        )
        self.add_recipe_file(
            name="tnt_minecart",
            data=datapack_utils.create_shaped_crafting_recipe(
                [
                    "ICI",
                    "III"
                ],
                {
                    "I": {"item": "minecraft:iron_ingot"},
                    "C": {"item": "minecraft:tnt"}
                },
                "minecraft:tnt_minecart", 1
            )
        )
        self.add_recipe_file(
            name="enchanted_golden_apple",
            data=datapack_utils.create_shaped_crafting_recipe(
                [
                    "GGG",
                    "GAG",
                    "GGG"
                ],
                {
                    "G": {"item": "minecraft:gold_block"},
                    "A": {"item": "minecraft:apple"}
                },
                "minecraft:enchanted_golden_apple", 1
            )
        )
        self.add_recipe_file(
            name="saddle",
            data=datapack_utils.create_shaped_crafting_recipe(
                [
                    "LLL",
                    "HLH"
                ],
                {
                    "L": {"item": "minecraft:leather"},
                    "H": {"item": "minecraft:tripwire_hook"}
                },
                "minecraft:saddle", 1
            )
        )
        self.add_recipe_file(
            name="white_wool",
            data=datapack_utils.create_shaped_crafting_recipe(
                [
                    "WWW",
                    "WDW",
                    "WWW"
                ],
                {
                    "D": {"item": "minecraft:white_dye"},
                    "W": {"tag": "minecraft:wool"}
                },
                "minecraft:white_wool", 8
            )
        )
        self.add_recipe_file(
            name="grass_block",
            data=datapack_utils.create_shaped_crafting_recipe(
                [
                    "G",
                    "D"
                ],
                {
                    "G": {"item": "minecraft:grass"},
                    "D": {"item": "minecraft:dirt"}
                },
                "minecraft:grass_block", 1
            )
        )
        self.add_recipe_file(
            name="snow_block",
            data=datapack_utils.create_shaped_crafting_recipe(
                [
                    "SS",
                    "SS"
                ],
                {
                    "S": {"item": "minecraft:snow"}
                },
                "minecraft:snow_block", 1
            )
        )

    def _shapeless_recipes(self):
        self.add_recipe_file(
            name="book",
            data=datapack_utils.create_shapeless_crafting_recipe(
                [
                    "minecraft:leather",
                    "minecraft:sugar_cane",
                    "minecraft:sugar_cane",
                    "minecraft:sugar_cane"
                ],
                "minecraft:book", 1
            )
        )
        self.add_recipe_file(
            name="bone_block",
            data=datapack_utils.create_shapeless_crafting_recipe(
                [
                    "minecraft:bone",
                    "minecraft:bone",
                    "minecraft:bone"
                ],
                "minecraft:bone_block", 1
            )
        )
        self.add_recipe_file(
            name="clay_ball",
            data=datapack_utils.create_shapeless_crafting_recipe(
                [
                    "minecraft:clay"
                ],
                "minecraft:clay_ball", 4
            )
        )
        self.add_recipe_file(
            name="honeycomb",
            data=datapack_utils.create_shapeless_crafting_recipe(
                [
                    "minecraft:honeycomb_block"
                ],
                "minecraft:honeycomb", 4
            )
        )
        self.add_recipe_file(
            name="brick",
            data=datapack_utils.create_shapeless_crafting_recipe(
                [
                    "minecraft:bricks"
                ],
                "minecraft:brick", 4
            )
        )
        self.add_recipe_file(
            name="quartz",
            data=datapack_utils.create_shapeless_crafting_recipe(
                [
                    "minecraft:quartz_block"
                ],
                "minecraft:quartz", 4
            )
        )
        self.add_recipe_file(
            name="glass",
            data=datapack_utils.create_shapeless_crafting_recipe(
                [
                    "minecraft:glowstone"
                ],
                "minecraft:glowstone_dust", 4
            )
        )
        self.add_recipe_file(
            name="flint",
            data=datapack_utils.create_shapeless_crafting_recipe(
                [
                    "minecraft:gravel"
                ],
                "minecraft:flint", 1
            )
        )
        self.add_recipe_file(
            name="name_tag",
            data=datapack_utils.create_shapeless_crafting_recipe(
                [
                    "minecraft:lead",
                    "minecraft:paper"
                ],
                "minecraft:name_tag", 1
            )
        )
        self.add_recipe_file(
            name="string",
            data=datapack_utils.create_shapeless_crafting_recipe(
                [
                    "minecraft:white_wool"
                ],
                "minecraft:string", 4
            )
        )
        self.add_recipe_file(
            name="ice",
            data=datapack_utils.create_shapeless_crafting_recipe(
                [
                    "minecraft:packed_ice"
                ],
                "minecraft:ice", 9
            )
        )
        self.add_recipe_file(
            name="packed_ice",
            data=datapack_utils.create_shapeless_crafting_recipe(
                [
                    "minecraft:blue_ice"
                ],
                "minecraft:packed_ice", 9
            )
        )

    def _smoking_recipes(self):
        self.add_recipe_file(
            name="smoking_leather",
            data=datapack_utils.create_smoking_recipe(
                [
                    "minecraft:rotten_flesh"
                ],
                "minecraft:leather"
            )
        )
