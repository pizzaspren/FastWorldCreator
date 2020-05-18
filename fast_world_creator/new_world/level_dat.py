import random

from nbtlib import tag, schema, nbt, parse_nbt

from fast_world_creator.utils import version_mapping

LevelData = schema('LevelData', {
    'DataVersion': tag.Int,
    'DimensionData': schema('DimensionData', {
        '1': schema('EndData', {
            'DragonFight': schema('DragonFight', {
                'ExitPortalLocation': schema('ExitPortalLocation', {
                    'X': tag.Byte,
                    'Y': tag.Byte,
                    'Z': tag.Byte
                }),
                'Gateways': tag.List[tag.Int],
                'DragonKilled': tag.Byte,
                'DragonUUIDLeast': tag.Long,
                'DragonUUIDMost': tag.Long,
                'PreviouslyKilled': tag.Byte
            })
        })
    }),
    'version': tag.Int,
    'initialized': tag.Byte,
    'LevelName': tag.String,
    'generatorName': tag.String,
    'generatorVersion': tag.Int,
    'generatorOptions': tag.String,
    'RandomSeed': tag.Long,
    'MapFeatures': tag.Byte,
    'LastPlayed': tag.Long,
    'SizeOnDisk': tag.Long,
    'allowCommands': tag.Byte,
    'hardcore': tag.Byte,
    'GameType': tag.Int,
    'Difficulty': tag.Byte,
    'DifficultyLocked': tag.Byte,
    'Time': tag.Long,
    'DayTime': tag.Long,
    'SpawnX': tag.Int,
    'SpawnY': tag.Int,
    'SpawnZ': tag.Int,
    'BorderCenterX': tag.Double,
    'BorderCenterZ': tag.Double,
    'BorderSize': tag.Double,
    'BorderSafeZone': tag.Double,
    'BorderWarningBlocks': tag.Double,
    'BorderWarningTime': tag.Double,
    'BorderSizeLerpTarget': tag.Double,
    'BorderSizeLerpTime': tag.Long,
    'BorderDamagePerBlock': tag.Double,
    'raining': tag.Byte,
    'rainTime': tag.Int,
    'thundering': tag.Byte,
    'thunderTime': tag.Int,
    'clearWeatherTime': tag.Int,
    'Player': tag.Compound,
    'GameRules': schema('Gamerules', {
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
    }),
    'Version': schema('Version', {
        'Id': tag.Int,
        'Name': tag.String,
        'Snapshot': tag.Byte
    }),
    'DataPacks': schema('DataPacks', {
        'Enabled': tag.List[tag.String],
        'Disabled': tag.List[tag.String]
    })
})

LevelFileSchema = schema('LevelFileSchema', {
    '': schema('LevelFileRoot', {
        'Data': LevelData
    })
})


class LevelFile(nbt.File, LevelFileSchema):
    @property
    def data(self):
        """The level data tag."""
        return self.root['Data']

    @data.setter
    def data(self, value):
        self.root['Data'] = value

    @classmethod
    def load(cls, filename, **kwargs):
        return super().load(filename, True)

    def __enter__(self):
        return self.data

    @staticmethod
    def from_arguments(arg_dict):
        """ Builds an nbt level.dat file from a template with arguments. """
        if arg_dict is None:
            arg_dict = {}
        default_seed = random.randint(0, 1000000)
        default_data = get_level_dat_template()
        default_args = {
            "arg_v_id": "0",
            "arg_version": "1.15.2",
            "arg_world_name": f"New_World_{default_seed}",
            "arg_seed": str(default_seed),
            "arg_hardcore": "0",
            "arg_diff": "2"
        }
        default_args.update(arg_dict)
        version_id = version_mapping.map[default_args["arg_version"]]
        default_args["arg_v_id"] = version_id
        default_args["arg_seed"] = str(int(default_seed))
        for key, val in default_args.items():
            default_data = default_data.replace(key, val)
        nbt_data = parse_nbt(default_data)
        return LevelFile(nbt_data, gzipped=True)


def get_level_dat_template():
    """ Gets the minimum template values for a level.dat file. """
    return """
    {"": {
        Data: {
            DataVersion: arg_v_id,
            version: 19133,
            initialized: 0b,
            LevelName: arg_world_name,
            generatorName: "default",
            generatorVersion: 1,
            RandomSeed: arg_seedL,
            allowCommands: 1b,
            Version: {
                Snapshot: 0b,
                Id: arg_v_id,
                Name: arg_version
            },
            DataPacks: {
                Enabled: [datapack_list]
            },
            hardcore: arg_hardcoreb,
            Difficulty: arg_diffb,
            GameRules: arg_gamerules
        }
    }}
    """


def get_default_gamerules():
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


if __name__ == "__main__":
    lf = LevelFile.from_arguments(None)
    print(lf)
