from datapack_creator.elements.datapacks.base_datapack import Datapack
from datapack_creator.elements.recipes import SmokingRecipe, \
    ShapelessCraftingRecipe, ShapedCraftingRecipe
from datapack_creator.minecraft.items import McItems
from datapack_creator.minecraft.tags.item_tags import McItemTags


class ConvenientCraftingDataPack(Datapack):
    name = "convenient_crafting"
    description = "Convenient and balanced crafting recipes"

    def __init__(self):
        super().__init__()

    def _shaped_recipes(self):
        self.add_element(ShapedCraftingRecipe(
            "iron_ingot",
            [
                "III",
                "ICI",
                "III"
            ],
            {
                "I": McItems.IRON_ORE.as_ingredient(),
                "C": McItemTags.COALS.as_ingredient()
            },
            McItems.IRON_INGOT, 8
        ))
        self.add_element(ShapedCraftingRecipe(
            "gold_ingot",
            [
                "III",
                "ICI",
                "III"
            ],
            {
                "I": McItems.GOLD_ORE.as_ingredient(),
                "C": McItemTags.COALS.as_ingredient()
            },
            McItems.GOLD_INGOT, 8
        ))
        self.add_element(ShapedCraftingRecipe(
            "diamond", [
                "III",
                "ICI",
                "III"
            ],
            {
                "I": McItems.DIAMOND_ORE.as_ingredient(),
                "C": McItemTags.COALS.as_ingredient()
            },
            McItems.DIAMOND, 8
        ))
        self.add_element(ShapedCraftingRecipe(
            "quartz2",
            [
                "III",
                "ICI",
                "III"
            ],
            {
                "I": McItems.NETHER_QUARTZ_ORE.as_ingredient(),
                "C": McItemTags.COALS.as_ingredient()
            },
            McItems.QUARTZ, 8
        ))
        self.add_element(ShapedCraftingRecipe(
            "lapis_lazuli",
            [
                "III",
                "ICI",
                "III"
            ],
            {
                "I": McItems.LAPIS_ORE.as_ingredient(),
                "C": McItemTags.COALS.as_ingredient()
            },
            McItems.LAPIS_LAZULI, 8
        ))
        self.add_element(ShapedCraftingRecipe(
            "redstone",
            [
                "III",
                "ICI",
                "III"
            ],
            {
                "I": McItems.REDSTONE_ORE.as_ingredient(),
                "C": McItemTags.COALS.as_ingredient()
            },
            McItems.REDSTONE, 8
        ))
        self.add_element(ShapedCraftingRecipe(
            "charcoal",
            [
                "III",
                "ICI",
                "III"
            ],
            {
                "I": McItemTags.LOGS_THAT_BURN.as_ingredient(),
                "C": McItemTags.COALS.as_ingredient()
            },
            McItems.CHARCOAL, 8
        ))
        self.add_element(ShapedCraftingRecipe(
            "chest_minecart",
            [
                "ICI",
                "III"
            ],
            {
                "I": McItems.IRON_INGOT.as_ingredient(),
                "C": McItems.CHEST.as_ingredient()
            },
            McItems.CHEST_MINECART, 1
        ))
        self.add_element(ShapedCraftingRecipe(
            "furnace_minecart",
            [
                "ICI",
                "III"
            ],
            {
                "I": McItems.IRON_INGOT.as_ingredient(),
                "C": McItems.FURNACE.as_ingredient()
            },
            McItems.FURNACE_MINECART, 1
        ))
        self.add_element(ShapedCraftingRecipe(
            "hopper_minecart",
            [
                "ICI",
                "III"
            ],
            {
                "I": McItems.IRON_INGOT.as_ingredient(),
                "C": McItems.HOPPER.as_ingredient()
            },
            McItems.HOPPER_MINECART, 1
        ))
        self.add_element(ShapedCraftingRecipe(
            "tnt_minecart",
            [
                "ICI",
                "III"
            ],
            {
                "I": McItems.IRON_INGOT.as_ingredient(),
                "C": McItems.TNT.as_ingredient()
            },
            McItems.TNT_MINECART, 1
        ))
        self.add_element(ShapedCraftingRecipe(
            "enchanted_golden_apple",
            [
                "GGG",
                "GAG",
                "GGG"
            ],
            {
                "G": McItems.GOLD_BLOCK.as_ingredient(),
                "A": McItems.APPLE.as_ingredient()
            },
            McItems.ENCHANTED_GOLDEN_APPLE, 1
        ))
        self.add_element(ShapedCraftingRecipe(
            "saddle",
            [
                "LLL",
                "HLH"
            ],
            {
                "L": McItems.LEATHER.as_ingredient(),
                "H": McItems.TRIPWIRE_HOOK.as_ingredient()
            },
            McItems.SADDLE, 1
        ))
        self.add_element(ShapedCraftingRecipe(
            "white_wool",
            [
                "WWW",
                "WDW",
                "WWW"
            ],
            {
                "D": McItems.WHITE_DYE.as_ingredient(),
                "W": McItemTags.WOOL.as_ingredient()
            },
            McItems.WHITE_WOOL, 8
        ))
        self.add_element(ShapedCraftingRecipe(
            "grass_block",
            [
                "G",
                "D"
            ],
            {
                "G": McItems.GRASS.as_ingredient(),
                "D": McItems.DIRT.as_ingredient()
            },
            McItems.GRASS_BLOCK, 1
        ))
        self.add_element(ShapedCraftingRecipe(
            "snow_block",
            [
                "SS",
                "SS"
            ],
            {
                "S": McItems.SNOW.as_ingredient()
            },
            McItems.SNOW_BLOCK, 1
        ))

    def _shapeless_recipes(self):
        self.add_element(ShapelessCraftingRecipe(
            "book",
            McItems.LEATHER * 1 + McItems.SUGAR_CANE * 3,
            McItems.BOOK, 1
        ))
        self.add_element(ShapelessCraftingRecipe(
            "bone_block",
            McItems.BONE * 3,
            McItems.BONE_BLOCK, 1
        ))
        self.add_element(ShapelessCraftingRecipe(
            "clay_ball",
            McItems.CLAY * 1,
            McItems.CLAY_BALL, 4
        ))
        self.add_element(ShapelessCraftingRecipe(
            "honeycomb",
            McItems.HONEYCOMB_BLOCK * 1,
            McItems.HONEYCOMB, 4
        ))
        self.add_element(ShapelessCraftingRecipe(
            "brick",
            McItems.BRICKS * 1,
            McItems.BRICK, 4
        ))
        self.add_element(ShapelessCraftingRecipe(
            "quartz",
            McItems.QUARTZ_BLOCK * 1,
            McItems.QUARTZ, 4
        ))
        self.add_element(ShapelessCraftingRecipe(
            "glass",
            McItems.GLOWSTONE * 1,
            McItems.GLOWSTONE_DUST, 4
        ))
        self.add_element(ShapelessCraftingRecipe(
            "flint",
            McItems.GRAVEL * 1,
            McItems.FLINT, 1
        ))
        self.add_element(ShapelessCraftingRecipe(
            "name_tag",
            McItems.LEAD * 1 + McItems.PAPER * 1,
            McItems.NAME_TAG, 1
        ))
        self.add_element(ShapelessCraftingRecipe(
            "string",
            McItems.WHITE_WOOL * 1,
            McItems.STRING, 4
        ))
        self.add_element(ShapelessCraftingRecipe(
            "ice",
            McItems.PACKED_ICE * 1,
            McItems.ICE, 9
        ))
        self.add_element(ShapelessCraftingRecipe(
            "packed_ice",
            McItems.BLUE_ICE * 1,
            McItems.PACKED_ICE, 9
        ))

        self.add_element(ShapelessCraftingRecipe(
            "coalblock",
            McItems.CHARCOAL * 9,
            McItems.COAL_BLOCK, 1
        ))

    def _smoking_recipes(self):
        self.add_element(SmokingRecipe(
            "smoking_leather",
            McItems.ROTTEN_FLESH.as_ingredient(),
            McItems.LEATHER
        ))
