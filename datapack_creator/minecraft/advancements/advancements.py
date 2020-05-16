from datapack_creator.elements.advancements import Advancement
from datapack_creator.minecraft.advancements import McAdvancementGroups


class McAdvancements:
    class Adventure:
        ADVENTURE = Advancement(
            f"{McAdvancementGroups.AG_ADVENTURE}/root")
        VOLUNTARY_EXILE = Advancement(
            f"{McAdvancementGroups.AG_ADVENTURE}/voluntary_exile")
        MONSTER_HUNTER = Advancement(
            f"{McAdvancementGroups.AG_ADVENTURE}/kill_a_mob")
        WHAT_A_DEAL = Advancement(
            f"{McAdvancementGroups.AG_ADVENTURE}/trade")
        STICKY_SITUATION = Advancement(
            f"{McAdvancementGroups.AG_ADVENTURE}/honey_block_slide")
        OL_BETSY = Advancement(
            f"{McAdvancementGroups.AG_ADVENTURE}/ol_betsy")
        SWEET_DREAMS = Advancement(
            f"{McAdvancementGroups.AG_ADVENTURE}/sleep_in_bed")
        HERO_OF_THE_VILLAGE = Advancement(
            f"{McAdvancementGroups.AG_ADVENTURE}/hero_of_the_village")
        A_THROWAWAY_JOKE = Advancement(
            f"{McAdvancementGroups.AG_ADVENTURE}/throw_trident")
        TAKE_AIM = Advancement(
            f"{McAdvancementGroups.AG_ADVENTURE}/shoot_arrow")
        MONSTERS_HUNTED = Advancement(
            f"{McAdvancementGroups.AG_ADVENTURE}/kill_all_mobs")
        POSTMORTAL = Advancement(
            f"{McAdvancementGroups.AG_ADVENTURE}/totem_of_undying")
        HIRED_HELP = Advancement(
            f"{McAdvancementGroups.AG_ADVENTURE}/summon_iron_golem")
        TWO_BIRDS_ONE_ARROW = Advancement(
            f"{McAdvancementGroups.AG_ADVENTURE}/two_birds_one_arrow")
        WHOS_THE_PILLAGER_NOW = Advancement(
            f"{McAdvancementGroups.AG_ADVENTURE}/whos_the_pillager_now")
        ARBALISTIC = Advancement(
            f"{McAdvancementGroups.AG_ADVENTURE}/arbalistic")
        ADVENTURING_TIME = Advancement(
            f"{McAdvancementGroups.AG_ADVENTURE}/adventuring_time")
        VERY_VERY_FRIGHTENING = Advancement(
            f"{McAdvancementGroups.AG_ADVENTURE}/very_very_frightening")
        SNIPER_DUEL = Advancement(
            f"{McAdvancementGroups.AG_ADVENTURE}/sniper_duel")
        BULLSEYE = Advancement(
            f"{McAdvancementGroups.AG_ADVENTURE}/bullseye")

    class End:
        THE_END = Advancement(
            f"{McAdvancementGroups.AG_END}/root")
        FREE_THE_END = Advancement(
            f"{McAdvancementGroups.AG_END}/kill_dragon")
        THE_NEXT_GENERATION = Advancement(
            f"{McAdvancementGroups.AG_END}/dragon_egg")
        REMOTE_GATEWAY = Advancement(
            f"{McAdvancementGroups.AG_END}/enter_end_gateway")
        THE_END_AGAIN = Advancement(
            f"{McAdvancementGroups.AG_END}/respawn_dragon")
        YOU_NEED_A_MINT = Advancement(
            f"{McAdvancementGroups.AG_END}/dragon_breath")
        THE_CITY_AT_THE_END_OF_THE_GAME = Advancement(
            f"{McAdvancementGroups.AG_END}/find_end_city")
        SKYS_THE_LIMIT = Advancement(
            f"{McAdvancementGroups.AG_END}/elytra")
        GREAT_VIEW_FROM_UP_HERE = Advancement(
            f"{McAdvancementGroups.AG_END}/levitate")

    class Nether:
        NETHER = Advancement(
            f"{McAdvancementGroups.AG_NETHER}/root")
        RETURN_TO_SENDER = Advancement(
            f"{McAdvancementGroups.AG_NETHER}/return_to_sender")
        SUBSPACE_BUBBLE = Advancement(
            f"{McAdvancementGroups.AG_NETHER}/fast_travel")
        A_TERRIBLE_FORTRESS = Advancement(
            f"{McAdvancementGroups.AG_NETHER}/find_fortress")
        UNEASY_ALLIANCE = Advancement(
            f"{McAdvancementGroups.AG_NETHER}/uneasy_alliance")
        SPOOKY_SCARY_SKELETONS = Advancement(
            f"{McAdvancementGroups.AG_NETHER}/get_wither_skull")
        INTO_FIRE = Advancement(
            f"{McAdvancementGroups.AG_NETHER}/obtain_blaze_rod")
        WITHERING_HEIGHTS = Advancement(
            f"{McAdvancementGroups.AG_NETHER}/summon_wither")
        LOCAL_BREWERY = Advancement(
            f"{McAdvancementGroups.AG_NETHER}/brew_potion")
        BRING_HOME_THE_BEACON = Advancement(
            f"{McAdvancementGroups.AG_NETHER}/create_beacon")
        BEACONATOR = Advancement(
            f"{McAdvancementGroups.AG_NETHER}/create_full_beacon")
        A_FURIOUS_COCTAIL = Advancement(
            f"{McAdvancementGroups.AG_NETHER}/all_potions")
        HOW_DID_WE_GET_HERE = Advancement(
            f"{McAdvancementGroups.AG_NETHER}/all_effects")
        HIDDEN_IN_THE_DEPTHS = Advancement(
            f"{McAdvancementGroups.AG_NETHER}/obtain_ancient_debris")
        COVER_ME_IN_DEBRIS = Advancement(
            f"{McAdvancementGroups.AG_NETHER}/netherite_armor")
        COUNTRY_LODE_TAKE_ME_HOME = Advancement(
            f"{McAdvancementGroups.AG_NETHER}/use_lodestone")
        WHO_IS_CUTTING_ONIONS = Advancement(
            f"{McAdvancementGroups.AG_NETHER}/obtain_crying_obsidian")
        NOT_QUITE_NINE_LIVES = Advancement(
            f"{McAdvancementGroups.AG_NETHER}/charge_respawn_anchor")
        THIS_BOAT_HAS_LEGS = Advancement(
            f"{McAdvancementGroups.AG_NETHER}/ride_strider")
        HOT_TOURIST_DESTINATIONS = Advancement(
            f"{McAdvancementGroups.AG_NETHER}/explore_nether")
        THOSE_WERE_THE_DAYS = Advancement(
            f"{McAdvancementGroups.AG_NETHER}/find_bastion")
        WAR_PIGS = Advancement(
            f"{McAdvancementGroups.AG_NETHER}/loot_bastion")
        OH_SHINY = Advancement(
            f"{McAdvancementGroups.AG_NETHER}/distract_piglin")

    class Story:
        MINECRAFT = Advancement(
            f"{McAdvancementGroups.AG_STORY}/root")
        STONE_AGE = Advancement(
            f"{McAdvancementGroups.AG_STORY}/mine_stone")
        GETTING_AN_UPGRADE = Advancement(
            f"{McAdvancementGroups.AG_STORY}/upgrade_tools")
        ACQUIRE_HARDWARE = Advancement(
            f"{McAdvancementGroups.AG_STORY}/smelt_iron")
        SUIT_UP = Advancement(
            f"{McAdvancementGroups.AG_STORY}/obtain_armor")
        HOT_STUFF = Advancement(
            f"{McAdvancementGroups.AG_STORY}/lava_bucket")
        ISNT_IT_IRON_PICK = Advancement(
            f"{McAdvancementGroups.AG_STORY}/iron_tools")
        NOT_TODAY_THANK_YOU = Advancement(
            f"{McAdvancementGroups.AG_STORY}/deflect_arrow")
        ICE_BUCKET_CHALLENGE = Advancement(
            f"{McAdvancementGroups.AG_STORY}/form_obsidian")
        DIAMONDS = Advancement(
            f"{McAdvancementGroups.AG_STORY}/mine_diamond")
        WE_NEED_TO_GO_DEEPER = Advancement(
            f"{McAdvancementGroups.AG_STORY}/enter_the_nether")
        COVER_ME_WITH_DIAMONDS = Advancement(
            f"{McAdvancementGroups.AG_STORY}/shiny_gear")
        ENCHANTER = Advancement(
            f"{McAdvancementGroups.AG_STORY}/enchant_item")
        ZOMBIE_DOCTOR = Advancement(
            f"{McAdvancementGroups.AG_STORY}/cure_zombie_villager")
        EYE_SPY = Advancement(
            f"{McAdvancementGroups.AG_STORY}/follow_ender_eye")
        THE_END = Advancement(
            f"{McAdvancementGroups.AG_STORY}/enter_the_end")

    class Husbandry:
        HUSBANDRY = Advancement(
            f"{McAdvancementGroups.AG_HUSBANDRY}/root")
        BEE_OUR_GUEST = Advancement(
            f"{McAdvancementGroups.AG_HUSBANDRY}/safely_harvest_honey")
        THE_PARROTS_AND_THE_BATS = Advancement(
            f"{McAdvancementGroups.AG_HUSBANDRY}/breed_an_animal")
        BEST_FRIENDS_FOREVER = Advancement(
            f"{McAdvancementGroups.AG_HUSBANDRY}/tame_an_animal")
        FISHY_BUSINESS = Advancement(
            f"{McAdvancementGroups.AG_HUSBANDRY}/fishy_business")
        TOTAL_BEELOCATION = Advancement(
            f"{McAdvancementGroups.AG_HUSBANDRY}/silk_touch_nest")
        A_SEEDY_PLACE = Advancement(
            f"{McAdvancementGroups.AG_HUSBANDRY}/plant_seed")
        TWO_BY_TWO = Advancement(
            f"{McAdvancementGroups.AG_HUSBANDRY}/bred_all_animals")
        A_COMPLETE_CATALOGUE = Advancement(
            f"{McAdvancementGroups.AG_HUSBANDRY}/complete_catalogue")
        TACTICAL_FISHING = Advancement(
            f"{McAdvancementGroups.AG_HUSBANDRY}/tactical_fishing")
        A_BALANCED_DIET = Advancement(
            f"{McAdvancementGroups.AG_HUSBANDRY}/balanced_diet")
        SERIOUS_DEDICATION = Advancement(
            f"{McAdvancementGroups.AG_HUSBANDRY}/break_diamond_hoe")
