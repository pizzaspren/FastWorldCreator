from __future__ import annotations

import json

from nbtlib import tag, schema, nbt, parse_nbt, InvalidLiteral

from fast_world_creator.utils.level_dat_utils import get_template_dict

xyz_dict = {
    'X': tag.Byte,
    'Y': tag.Byte,
    'Z': tag.Byte
}
dragon_fight_dict = {
    'ExitPortalLocation': schema('ExitPortalLocation', xyz_dict),
    'Gateways': tag.List[tag.Int],
    'DragonKilled': tag.Byte,
    'DragonUUIDLeast': tag.Long,
    'DragonUUIDMost': tag.Long,
    'PreviouslyKilled': tag.Byte
}
end_data_dict = {
    'DragonFight': schema('DragonFight', dragon_fight_dict)
}
dimension_data_dict = {
    '1': schema('EndData', end_data_dict)
}
game_rule_dict = {
    'announceAdvancements': tag.String,
    'commandBlockOutput': tag.String,
    'disableElytraMovementCheck': tag.String,
    'disableRaids': tag.String,
    'doDaylightCycle': tag.String,
    'doEntityDrops': tag.String,
    'doFireTick': tag.String,
    'doInsomnia': tag.String,
    'doImmediateRespawn': tag.String,
    'doLimitedCrafting': tag.String,
    'doMobLoot': tag.String,
    'doMobSpawning': tag.String,
    'doPatrolSpawning': tag.String,
    'doTileDrops': tag.String,
    'doTraderSpawning': tag.String,
    'doWeatherCycle': tag.String,
    'drowningDamage': tag.String,
    'fallDamage': tag.String,
    'fireDamage': tag.String,
    'keepInventory': tag.String,
    'logAdminCommands': tag.String,
    'maxCommandChainLength': tag.String,
    'maxEntityCramming': tag.String,
    'mobGriefing': tag.String,
    'naturalRegeneration': tag.String,
    'randomTickSpeed': tag.String,
    'reducedDebugInfo': tag.String,
    'sendCommandFeedback': tag.String,
    'showDeathMessages': tag.String,
    'spawnRadius': tag.String,
    'spectatorsGenerateChunks': tag.String,
}
version_dict = {
    'Id': tag.Int,
    'Name': tag.String,
    'Snapshot': tag.Byte
}
datapacks_dict = {
    'Enabled': tag.List[tag.String],
    'Disabled': tag.List[tag.String]
}
generator_options_dict = {
    'biome_source': schema("biome_sources", {
        'options': schema("biome_source_options", {
            'biomes': tag.List[tag.String],
            'size': tag.Byte
        }),
        'type': tag.String
    }),
    'chunk_generator': schema("chunk_generator", {
        'options': schema("chunk_generator_options", {
            'default_block': tag.String,
            'default_fluid': tag.String
        }),
        'type': tag.String
    }),
    'structures': tag.Compound,
    'layers': tag.List[schema('layers', {
        'block': tag.String,
        'height': tag.String
    })]
}
level_data_dict = {
    'allowCommands': tag.Byte,
    'BorderCenterX': tag.Double,
    'BorderCenterZ': tag.Double,
    'BorderDamagePerBlock': tag.Double,
    'BorderSafeZone': tag.Double,
    'BorderSize': tag.Double,
    'BorderSizeLerpTarget': tag.Double,
    'BorderSizeLerpTime': tag.Long,
    'BorderWarningBlocks': tag.Double,
    'BorderWarningTime': tag.Double,
    'clearWeatherTime': tag.Int,
    'DataPacks': schema('DataPacks', datapacks_dict, strict=True),
    'DataVersion': tag.Int,
    'DayTime': tag.Long,
    'Difficulty': tag.Byte,
    'DifficultyLocked': tag.Byte,
    'DimensionData': schema('DimensionData', dimension_data_dict, strict=True),
    'GameRules': tag.Compound,
    'GameType': tag.Int,
    'generatorName': tag.String,
    'generatorOptions': schema('generatorOptions', generator_options_dict,
                               strict=True),
    'generatorVersion': tag.Int,
    'hardcore': tag.Byte,
    'initialized': tag.Byte,
    'LastPlayed': tag.Long,
    'LevelName': tag.String,
    'MapFeatures': tag.Byte,
    'Player': tag.Compound,
    'raining': tag.Byte,
    'rainTime': tag.Int,
    'RandomSeed': tag.Long,
    'SizeOnDisk': tag.Long,
    'SpawnX': tag.Int,
    'SpawnY': tag.Int,
    'SpawnZ': tag.Int,
    'thundering': tag.Byte,
    'thunderTime': tag.Int,
    'Time': tag.Long,
    'version': tag.Int,
    'Version': schema('Version', version_dict, strict=True)
}

LevelDataSchema = schema('LevelData', level_data_dict, strict=True)
LevelFileSchema = schema('LevelFileSchema', {
    '': schema('LevelFileRoot', {
        'Data': tag.Compound
    })
})


class LevelFile(nbt.File, LevelFileSchema):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gzipped = True

    @property
    def data(self) -> schema:
        """The level data tag."""
        return self.root['Data']

    @data.setter
    def data(self, value: schema) -> None:
        self.root['Data'] = value

    @classmethod
    def load(cls, filename: str, **kwargs) -> nbt.File:
        return super().load(filename, True)

    @staticmethod
    def from_arguments(arg_dict: dict) -> LevelFile:
        """  Builds an nbt level.dat file from a template with arguments.

        :param arg_dict: The dictionary containing the values for a data schema.
        :return: The created nbt file object.
        """
        default_data = get_template_dict()
        default_data.update(arg_dict)
        # Why Mojang?
        default_data["DataVersion"] = default_data["Version"]["Id"]

        level_file = LevelFile(parse_nbt("{'':{Data:{}}}"))
        level_file.data = LevelDataSchema(parse_nbt(json.dumps(default_data)))
        return level_file
