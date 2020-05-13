from fast_world_creator.datapacks.datapack_base import Datapack
from fast_world_creator.minecraft.advancements import *


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
        self.add_advancement(Advancement(
            name="enchant_item_30",
            datapack=self.name,
            icon_item="minecraft:experience_bottle",
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
                            "scores": [{
                                "level": {
                                    "min": 30
                                }
                            }],
                            "entity": "this"
                        }]
                    }
                }
            }
        ))

    def _create_adventure_advancements(self):
        self.add_advancement(Advancement(
            name="snow_golem",
            datapack=self.name,
            icon_item="minecraft:jack_o_lantern",
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
            datapack=self.name,
            icon_item="minecraft:trident",
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
        self.add_advancement(charge_creeper)
        zombie_head = Advancement(
            name="zombie_head",
            datapack=self.name,
            icon_item="minecraft:zombie_head",
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
                                    "min": 1
                                }
                            }
                        ]
                    }
                }
            }
        )
        self.add_advancement(zombie_head)
        self.add_advancement(Advancement(
            name="skeleton_skull",
            datapack=self.name,
            icon_item="minecraft:skeleton_skull",
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
                                    "min": 1
                                }
                            }
                        ]
                    }
                }
            }
        ))
        self.add_advancement(Advancement(
            name="creeper_head",
            datapack=self.name,
            group="adventure",
            icon_item="minecraft:creeper_head",
            title="SSSsss...",
            description="Obtain a Creeper head",
            parent=charge_creeper,
            criteria={
                "creeper_head": {
                    "trigger": "minecraft:inventory_changed",
                    "conditions": {
                        "items": [
                            {
                                "item": "minecraft:creeper_head",
                                "count": {
                                    "min": 1
                                }
                            }
                        ]
                    }
                }
            }
        ))

    def _create_husbandry_advancements(self):
        self.add_advancement(Advancement(
            name="fish_enchanted_book",
            datapack=self.name,
            icon_item="minecraft:enchanted_book",
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
        self.add_advancement(Advancement(
            name="nether_roof",
            datapack=self.name,
            icon_item="minecraft:bedrock",
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
                                "min": 128
                            }
                        }
                    }
                }
            }
        ))

    def _create_end_advancements(self):
        self.add_advancement(Advancement(
            name="fall_into_void",
            datapack=self.name,
            icon_item="minecraft:feather",
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
            datapack=self.name,
            icon_item="minecraft:chorus_fruit",
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
        self.add_advancement(eat_chorus)
        self.add_advancement(Advancement(
            name="plant_chorus",
            datapack=self.name,
            icon_item="minecraft:chorus_flower",
            title="Reforestation",
            description="Plant a Chorus flower on End stone",
            parent=eat_chorus,
            criteria={
                "plant_chorus": {
                    "trigger": "minecraft:placed_block",
                    "block": {
                        "item": "minecraft:chorus_flower"
                    }
                }
            }
        ))
        self.add_advancement(Advancement(
            name="craft_shulker_box",
            datapack=self.name,
            icon_item="minecraft:shulker_box",
            title="Portable storage",
            description="Craft a Shulker Box",
            parent=McAdvancements.End.THE_CITY_AT_THE_END_OF_THE_GAME,
            criteria={
                "craft_shulker_box": {
                    "trigger": "minecraft:inventory_changed",
                    "items": {
                        "item": "minecraft:shulker_box",
                        "count": {
                            "min": 1,
                            "max": 64
                        }
                    },
                    "player": {
                        "entity_scores": {
                            "entity": "this",
                            "scores": [
                                {
                                    "minecraft.crafted:minecraft.shulker_box": {
                                        "min": 1
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        ))
        self.add_advancement(Advancement(
            name="find_dragon_head",
            datapack=self.name,
            icon_item="minecraft:dragon_head",
            title="End souvenir",
            description="Obtain a Dragon Head",
            parent=McAdvancements.End.THE_CITY_AT_THE_END_OF_THE_GAME,
            criteria={
                "find_dragon_head": {
                    "trigger": "minecraft:inventory_changed",
                    "items": {
                        "item": "minecraft:dragon_head",
                        "count": {
                            "min": 1
                        }
                    }
                }
            }
        ))
        self.add_advancement(Advancement(
            name="break_elytra",
            icon_item="minecraft:elytra",
            icon_nbt="{Damage:431}",
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
