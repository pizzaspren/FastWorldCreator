from datapack_creator.elements.advancements import AdvancementFrame, Advancement
from datapack_creator.elements.datapacks.base_datapack import Datapack
from datapack_creator.elements.item import Item
from datapack_creator.minecraft.advancements import McAdvancements


class MoreAdvancementsDataPack(Datapack):
    name = "more_advancements"
    description = "More advancements for your game"

    def __init__(self):
        super().__init__()
        self.needs_loot_tables = False

    def _create_advancements(self):
        self._create_story_advancements()
        self._create_adventure_advancements()
        self._create_husbandry_advancements()
        self._create_nether_advancements()
        self._create_end_advancements()

    def _create_story_advancements(self):
        self.add_element(Advancement(
            name="enchant_item_30",
            icon=Item("minecraft:experience_bottle"),
            title="Great enchanter",
            description="Enchant while being at least level 30",
            frame=AdvancementFrame.GOAL,
            parent=McAdvancements.Story.ENCHANTER,
            criteria={
                "enchant_item_30": {
                    "trigger": "minecraft:enchanted_item",
                    "conditions": {
                        "player": [{
                            "condition": "minecraft:entity_scores",
                            "scores": {
                                "level": {
                                    "min": 30,
                                    "max": 512
                                }
                            },
                            "entity": "this"
                        }]
                    }
                }
            }
        ))

    def _create_adventure_advancements(self):
        self.add_element(Advancement(
            name="snow_golem",
            icon=Item("minecraft:jack_o_lantern"),
            title="Snowy wonderland",
            description="Summon a snow golem",
            parent=McAdvancements.Adventure.ADVENTURE,
            criteria={
                "summon_snow_golem": {
                    "trigger": "minecraft:summoned_entity",
                    "conditions": {
                        "entity": {
                            "type": "minecraft:snow_golem"
                        }
                    }
                }
            }
        ))
        charge_creeper = Advancement(
            name="charge_creeper",
            icon=Item("minecraft:trident"),
            title="Uh Oh...",
            description="Strike a Creeper with lightning",
            parent=McAdvancements.Adventure.A_THROWAWAY_JOKE,
            criteria={
                "charge_creeper": {
                    "trigger": "minecraft:channeled_lightning",
                    "conditions": {
                        "entity": {
                            "type": "minecraft:creeper"
                        }
                    }
                }

            })
        self.add_element(charge_creeper)
        zombie_head = Advancement(
            name="zombie_head",
            icon=Item("minecraft:zombie_head"),
            title="Brains?",
            description="Obtain a Zombie head",
            parent=charge_creeper,
            criteria={
                "zombie_head": {
                    "trigger": "minecraft:inventory_changed",
                    "conditions": {
                        "items": [
                            {
                                "item": "minecraft:zombie_head",
                                "count": {
                                    "min": 1,
                                    "max": 64
                                }
                            }
                        ]
                    }
                }
            }
        )
        self.add_element(zombie_head)
        self.add_element(Advancement(
            name="skeleton_skull",
            icon=Item("minecraft:skeleton_skull"),
            title="Doot",
            description="Obtain a Skeleton skull",
            parent=charge_creeper,
            criteria={
                "skeleton_skull": {
                    "trigger": "minecraft:inventory_changed",
                    "conditions": {
                        "items": [
                            {
                                "item": "minecraft:skeleton_skull",
                                "count": {
                                    "min": 1,
                                    "max": 64
                                }
                            }
                        ]
                    }
                }
            }
        ))
        self.add_element(Advancement(
            name="creeper_head",
            group="adventure",
            icon=Item("minecraft:creeper_head"),
            title="SSSsss...",
            description="Obtain a Creeper head",
            parent=charge_creeper,
            criteria={
                "creeper_head": {
                    "trigger": "minecraft:inventory_changed",
                    "conditions": {
                        "items": [
                            {
                                "item": "minecraft:creeper_head"
                            }
                        ]
                    }
                }
            }
        ))

    def _create_husbandry_advancements(self):
        self.add_element(Advancement(
            name="fish_enchanted_book",
            icon=Item("minecraft:enchanted_book"),
            title="Magical catch",
            description="Fish an enchanted book",
            parent=McAdvancements.Husbandry.FISHY_BUSINESS,
            criteria={
                "fish_enchanted_book": {
                    "trigger": "minecraft:fishing_rod_hooked",
                    "conditions": {
                        "item": {
                            "item": "minecraft:enchanted_book"
                        }
                    }
                }
            }
        ))

    def _create_nether_advancements(self):
        self.add_element(Advancement(
            name="nether_roof",
            icon=Item("minecraft:bedrock"),
            title="Superflat!",
            description="Stand on the nether roof",
            frame=AdvancementFrame.CHALLENGE,
            hidden=True,
            parent=McAdvancements.Nether.NETHER,
            criteria={
                "nether_roof": {
                    "trigger": "minecraft:location",
                    "conditions": {
                        "dimension": "minecraft:nether",
                        "position": {
                            "y": {
                                "min": 128,
                                "max": 256
                            }
                        }
                    }
                }
            }
        ))

    def _create_end_advancements(self):
        self.add_element(Advancement(
            name="fall_into_void",
            icon=Item("minecraft:feather"),
            title="Stop, Drop and Void",
            description="Fall into the void",
            frame=AdvancementFrame.GOAL,
            hidden=True,
            parent=McAdvancements.End.THE_END,
            criteria={
                "fall_into_void": {
                    "trigger": "minecraft:location",
                    "conditions": {
                        "dimension": "minecraft:the_end",
                        "position": {
                            "y": -64
                        }
                    }
                }
            }
        ))
        eat_chorus = Advancement(
            name="eat_chorus",
            icon=Item("minecraft:chorus_fruit"),
            title="Zoop",
            description="Eat a Chorus fruit",
            parent=McAdvancements.End.THE_END,
            criteria={
                "eat_chorus": {
                    "trigger": "minecraft:consume_item",
                    "item": {
                        "item": "minecraft:chorus_fruit"
                    }
                }
            }
        )
        self.add_element(eat_chorus)
        self.add_element(Advancement(
            name="plant_chorus",
            icon=Item("minecraft:chorus_flower"),
            title="Reforestation",
            description="Plant a Chorus flower on End stone",
            parent=eat_chorus,
            criteria={
                "plant_chorus": {
                    "trigger": "minecraft:placed_block",
                    "conditions": {
                        "block": "minecraft:chorus_flower"
                    }
                }
            }
        ))
        self.add_element(Advancement(
            name="craft_shulker_box",
            icon=Item("minecraft:shulker_box"),
            title="Portable storage",
            description="Craft a Shulker Box",
            parent=McAdvancements.End.THE_CITY_AT_THE_END_OF_THE_GAME,
            criteria={
                "craft_shulker_box": {
                    "trigger": "minecraft:inventory_changed",
                    "conditions": {
                        "items": [
                            {
                                "item": "minecraft:shulker_box"
                            }
                        ]
                    }
                }
            }
        ))
        self.add_element(Advancement(
            name="find_dragon_head",
            icon=Item("minecraft:dragon_head"),
            title="End souvenir",
            description="Obtain a Dragon Head",
            parent=McAdvancements.End.THE_CITY_AT_THE_END_OF_THE_GAME,
            criteria={
                "find_dragon_head": {
                    "trigger": "minecraft:inventory_changed",
                    "conditions": {
                        "items": [
                            {
                                "item": "minecraft:dragon_head"
                            }
                        ]
                    }
                }
            }
        ))
        self.add_element(Advancement(
            name="break_elytra",
            icon=Item("minecraft:elytra", "{Damage:431}"),
            title="Durability's the Limit",
            description="Deplete an elytra's durability",
            parent=McAdvancements.End.SKYS_THE_LIMIT,
            criteria={
                "break_elytra": {
                    "trigger": "minecraft:item_durability_changed",
                    "conditions": {
                        "item": {
                            "item": "minecraft:elytra"
                        },
                        "durability": 1
                    }
                }
            }
        ))
