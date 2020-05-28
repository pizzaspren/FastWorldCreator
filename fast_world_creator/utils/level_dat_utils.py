def get_template_dict() -> dict:
    """ Get a template for the level.dat nbt structure.

    :return: A template for level.dat.
    """
    return {
        'allowCommands': 1,
        'BorderCenterX': 0,
        'BorderCenterZ': 0,
        'BorderDamagePerBlock': 0.2,
        'BorderSafeZone': 5,
        'BorderSize': 60000000,
        'BorderSizeLerpTarget': 60000000,
        'BorderSizeLerpTime': 0,
        'BorderWarningBlocks': 5,
        'BorderWarningTime': 15,
        'clearWeatherTime': 0,
        'DataPacks': {
            'Disabled': [],
            'Enabled': []
        },
        'DataVersion': 2230,
        'Difficulty': 2,
        'DifficultyLocked': 0,
        'DayTime': 3000,
        'GameType': 0,
        'GameRules': {},  # Always gets overwritten by rules from UI
        'generatorName': "default",
        # generatorOptions only present in Buffet and Superflat generators
        'generatorVersion': 0,
        'hardcore': 0,
        'initialized': 0,
        'LastPlayed': 0,
        'LevelName': 'FastWorldCreator_DefaultName',
        'MapFeatures': 1,
        'RandomSeed': 0,
        'raining': 0,
        'rainTime': 0,
        # SpawnX, SpawnY, SpawnZ disabled - Dangerous to set spawn manually
        'thundering': 0,
        'thunderTime': 0,
        'Time': 0,
        'version': 19133,
        'Version': {
            'Id': 2230,
            'Name': '1.15.2',
            'Snapshot': 0
        }
    }


def get_default_gamerules() -> dict:
    """ Get a dictionary containing each game rule and its default value.

    Game rules that are not present in a Minecraft version are ignored by the
    client so it is safe to use all the game rules regardless of the version.
    Default values found in https://minecraft.gamepedia.com/Commands/gamerule.
    :return: All the gamerules ever parsed in any Minecraft version between 1.13
        and 1.15.2
    """
    return {
        'announceAdvancements': True,
        'commandBlockOutput': True,
        'disableElytraMovementCheck': False,
        'disableRaids': False,
        'doDaylightCycle': True,
        'doEntityDrops': True,
        'doFireTick': True,
        'doInsomnia': True,
        'doImmediateRespawn': False,
        'doLimitedCrafting': False,
        'doMobLoot': True,
        'doMobSpawning': True,
        'doPatrolSpawning': True,
        'doTileDrops': True,
        'doTraderSpawning': True,
        'doWeatherCycle': True,
        'drowningDamage': True,
        'fallDamage': True,
        'fireDamage': True,
        'keepInventory': False,
        'logAdminCommands': True,
        'maxCommandChainLength': 65536,
        'maxEntityCramming': 24,
        'mobGriefing': True,
        'naturalRegeneration': True,
        'randomTickSpeed': 3,
        'reducedDebugInfo': False,
        'sendCommandFeedback': True,
        'showDeathMessages': True,
        'spawnRadius': 10,
        'spectatorsGenerateChunks': True,
    }
