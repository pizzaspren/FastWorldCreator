from __future__ import annotations

import json
from typing import List, Union


class AdvancementGroup:
    group = ""

    def __init__(self, group):
        self.group = group

    def __str__(self):
        return self.group

    def __repr__(self):
        return self.__str__()


AG_END = AdvancementGroup("end")
AG_NETHER = AdvancementGroup("nether")
AG_HUSBANDRY = AdvancementGroup("husbandry")
AG_STORY = AdvancementGroup("story")
AG_ADVENTURE = AdvancementGroup("adventure")


class AdvancementFrame:
    TASK = "task"
    GOAL = "goal"
    CHALLENGE = "challenge"


class Advancement:

    def __init__(self, name="empty", group=AG_STORY.group, datapack="minecraft",
                 frame=AdvancementFrame.TASK, icon_item="minecraft:grass_block",
                 icon_nbt="", title="Placeholder", background=None,
                 description="Placeholder", hidden=False, parent=None,
                 criteria=None, requirements=None, rewards=None):
        self.name = name.split("/")[-1]
        self.group = "/".join(name.split("/")[:-1]) or parent.group or group
        self.datapack = datapack

        self.frame = frame
        self.icon = dict(item=icon_item)
        if icon_nbt:
            self.icon["nbt"] = icon_nbt
        self.title = title
        self.background = background
        self.description = description
        self.hidden = hidden

        self.parent = parent

        self.criteria = criteria
        self.requirements = requirements
        self.rewards = rewards

    def __str__(self) -> str:
        return f"{self.datapack}:{self.group}/{self.name}"

    def set_frame(self, frame: AdvancementFrame) -> Advancement:
        self.frame = str(frame)
        return self

    def set_icon(self, icon: dict) -> Advancement:
        self.icon = icon
        return self

    def set_icon_item(self, item: str) -> Advancement:
        self.icon["item"] = item
        return self

    def set_icon_nbt(self, nbt: str) -> Advancement:
        self.icon["nbt"] = nbt
        return self

    def set_title(self, title: str) -> Advancement:
        self.title = title
        return self

    def set_background(self, background: str) -> Advancement:
        self.background = background
        return self

    def set_description(self, desc: str) -> Advancement:
        self.description = desc
        return self

    def set_is_hidden(self, hidden: bool) -> Advancement:
        self.hidden = hidden
        return self

    def set_parent(self, parent: Advancement) -> Advancement:
        self.parent = str(parent) or "root"
        self.group = parent.group
        return self

    def set_criteria(self, criteria: dict) -> Advancement:
        self.criteria = criteria
        return self

    def set_requirements(self, requirements: List[Union[List[str], str]]) -> Advancement:
        self.requirements = requirements
        return self

    def set_rewards(self, rewards: dict) -> Advancement:
        self.rewards = rewards
        return self

    def _get_display(self) -> dict:
        display = dict(
            icon=self.icon,
            title=self.title,
            frame=self.frame,
            description=self.description,
            hidden=self.hidden
        )
        if self.background:
            display["background"] = self.background
        return display

    def get_path(self) -> str:
        return f"data/{self.datapack}/advancements/{self.group}/{self.name}.json"

    def to_data(self) -> str:
        root_tag = dict()
        root_tag["display"] = self._get_display()
        if self.parent:
            root_tag["parent"] = str(self.parent)
        root_tag["criteria"] = self.criteria
        if self.requirements:
            root_tag["requirements"] = self.requirements
        if self.rewards:
            root_tag["rewards"] = self.rewards
        return json.dumps(root_tag)


class McAdvancements:
    class Adventure:
        ADVENTURE = Advancement(f"{AG_ADVENTURE}/root")
        VOLUNTARY_EXILE = Advancement(f"{AG_ADVENTURE}/voluntary_exile")
        MONSTER_HUNTER = Advancement(f"{AG_ADVENTURE}/kill_a_mob")
        WHAT_A_DEAL = Advancement(f"{AG_ADVENTURE}/trade")
        STICKY_SITUATION = Advancement(f"{AG_ADVENTURE}/honey_block_slide")
        OL_BETSY = Advancement(f"{AG_ADVENTURE}/ol_betsy")
        SWEET_DREAMS = Advancement(f"{AG_ADVENTURE}/sleep_in_bed")
        HERO_OF_THE_VILLAGE = Advancement(f"{AG_ADVENTURE}/hero_of_the_village")
        A_THROWAWAY_JOKE = Advancement(f"{AG_ADVENTURE}/throw_trident")
        TAKE_AIM = Advancement(f"{AG_ADVENTURE}/shoot_arrow")
        MONSTERS_HUNTED = Advancement(f"{AG_ADVENTURE}/kill_all_mobs")
        POSTMORTAL = Advancement(f"{AG_ADVENTURE}/totem_of_undying")
        HIRED_HELP = Advancement(f"{AG_ADVENTURE}/summon_iron_golem")
        TWO_BIRDS_ONE_ARROW = Advancement(f"{AG_ADVENTURE}/two_birds_one_arrow")
        WHOS_THE_PILLAGER_NOW = Advancement(f"{AG_ADVENTURE}/whos_the_pillager_now")
        ARBALISTIC = Advancement(f"{AG_ADVENTURE}/arbalistic")
        ADVENTURING_TIME = Advancement(f"{AG_ADVENTURE}/adventuring_time")
        VERY_VERY_FRIGHTENING = Advancement(f"{AG_ADVENTURE}/very_very_frightening")
        SNIPER_DUEL = Advancement(f"{AG_ADVENTURE}/sniper_duel")
        BULLSEYE = Advancement(f"{AG_ADVENTURE}/bullseye")

    class End:
        THE_END = Advancement(f"{AG_END}/root")
        FREE_THE_END = Advancement(f"{AG_END}/kill_dragon")
        THE_NEXT_GENERATION = Advancement(f"{AG_END}/dragon_egg")
        REMOTE_GATEWAY = Advancement(f"{AG_END}/enter_end_gateway")
        THE_END_AGAIN = Advancement(f"{AG_END}/respawn_dragon")
        YOU_NEED_A_MINT = Advancement(f"{AG_END}/dragon_breath")
        THE_CITY_AT_THE_END_OF_THE_GAME = Advancement(f"{AG_END}/find_end_city")
        SKYS_THE_LIMIT = Advancement(f"{AG_END}/elytra")
        GREAT_VIEW_FROM_UP_HERE = Advancement(f"{AG_END}/levitate")

    class Nether:
        NETHER = Advancement(f"{AG_NETHER}/root")
        RETURN_TO_SENDER = Advancement(f"{AG_NETHER}/return_to_sender")
        SUBSPACE_BUBBLE = Advancement(f"{AG_NETHER}/fast_travel")
        A_TERRIBLE_FORTRESS = Advancement(f"{AG_NETHER}/find_fortress")
        UNEASY_ALLIANCE = Advancement(f"{AG_NETHER}/uneasy_alliance")
        SPOOKY_SCARY_SKELETONS = Advancement(f"{AG_NETHER}/get_wither_skull")
        INTO_FIRE = Advancement(f"{AG_NETHER}/obtain_blaze_rod")
        WITHERING_HEIGHTS = Advancement(f"{AG_NETHER}/summon_wither")
        LOCAL_BREWERY = Advancement(f"{AG_NETHER}/brew_potion")
        BRING_HOME_THE_BEACON = Advancement(f"{AG_NETHER}/create_beacon")
        BEACONATOR = Advancement(f"{AG_NETHER}/create_full_beacon")
        A_FURIOUS_COCTAIL = Advancement(f"{AG_NETHER}/all_potions")
        HOW_DID_WE_GET_HERE = Advancement(f"{AG_NETHER}/all_effects")
        HIDDEN_IN_THE_DEPTHS = Advancement(f"{AG_NETHER}/obtain_ancient_debris")
        COVER_ME_IN_DEBRIS = Advancement(f"{AG_NETHER}/netherite_armor")
        COUNTRY_LODE_TAKE_ME_HOME = Advancement(f"{AG_NETHER}/use_lodestone")
        WHO_IS_CUTTING_ONIONS = Advancement(f"{AG_NETHER}/obtain_crying_obsidian")
        NOT_QUITE_NINE_LIVES = Advancement(f"{AG_NETHER}/charge_respawn_anchor")
        THIS_BOAT_HAS_LEGS = Advancement(f"{AG_NETHER}/ride_strider")
        HOT_TOURIST_DESTINATIONS = Advancement(f"{AG_NETHER}/explore_nether")
        THOSE_WERE_THE_DAYS = Advancement(f"{AG_NETHER}/find_bastion")
        WAR_PIGS = Advancement(f"{AG_NETHER}/loot_bastion")
        OH_SHINY = Advancement(f"{AG_NETHER}/distract_piglin")

    class Story:
        MINECRAFT = Advancement(f"{AG_STORY}/root")
        STONE_AGE = Advancement(f"{AG_STORY}/mine_stone")
        GETTING_AN_UPGRADE = Advancement(f"{AG_STORY}/upgrade_tools")
        ACQUIRE_HARDWARE = Advancement(f"{AG_STORY}/smelt_iron")
        SUIT_UP = Advancement(f"{AG_STORY}/obtain_armor")
        HOT_STUFF = Advancement(f"{AG_STORY}/lava_bucket")
        ISNT_IT_IRON_PICK = Advancement(f"{AG_STORY}/iron_tools")
        NOT_TODAY_THANK_YOU = Advancement(f"{AG_STORY}/deflect_arrow")
        ICE_BUCKET_CHALLENGE = Advancement(f"{AG_STORY}/form_obsidian")
        DIAMONDS = Advancement(f"{AG_STORY}/mine_diamond")
        WE_NEED_TO_GO_DEEPER = Advancement(f"{AG_STORY}/enter_the_nether")
        COVER_ME_WITH_DIAMONDS = Advancement(f"{AG_STORY}/shiny_gear")
        ENCHANTER = Advancement(f"{AG_STORY}/enchant_item")
        ZOMBIE_DOCTOR = Advancement(f"{AG_STORY}/cure_zombie_villager")
        EYE_SPY = Advancement(f"{AG_STORY}/follow_ender_eye")
        THE_END = Advancement(f"{AG_STORY}/enter_the_end")

    class Husbandry:
        HUSBANDRY = Advancement(f"{AG_HUSBANDRY}/root")
        BEE_OUR_GUEST = Advancement(f"{AG_HUSBANDRY}/safely_harvest_honey")
        THE_PARROTS_AND_THE_BATS = Advancement(f"{AG_HUSBANDRY}/breed_an_animal")
        BEST_FRIENDS_FOREVER = Advancement(f"{AG_HUSBANDRY}/tame_an_animal")
        FISHY_BUSINESS = Advancement(f"{AG_HUSBANDRY}/fishy_business")
        TOTAL_BEELOCATION = Advancement(f"{AG_HUSBANDRY}/silk_touch_nest")
        A_SEEDY_PLACE = Advancement(f"{AG_HUSBANDRY}/plant_seed")
        TWO_BY_TWO = Advancement(f"{AG_HUSBANDRY}/bred_all_animals")
        A_COMPLETE_CATALOGUE = Advancement(f"{AG_HUSBANDRY}/complete_catalogue")
        TACTICAL_FISHING = Advancement(f"{AG_HUSBANDRY}/tactical_fishing")
        A_BALANCED_DIET = Advancement(f"{AG_HUSBANDRY}/balanced_diet")
        SERIOUS_DEDICATION = Advancement(f"{AG_HUSBANDRY}/break_diamond_hoe")
