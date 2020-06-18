import logging
import os
from configparser import ConfigParser
from functools import lru_cache
from typing import Dict, List, Union

from fast_world_creator.datapacks.external_datapack import ExternalDatapack
from fast_world_creator.datapacks.random_loot import RandomLootDataPack
from fast_world_creator.utils import minecraft_utils as mu

MC_FOLDER = f"{os.getenv('APPDATA')}/.minecraft"


@lru_cache(maxsize=1)
def get_or_create_config() -> ConfigParser:
    """ Read the configuration file, or create it if not present.

    :return: The program configuration values.
    """
    cfg = ConfigParser()
    if not cfg.read('config.ini'):
        cfg["LOGGING"] = {
            "file": "output.log",
            "level": "INFO"
        }
        cfg["UI"] = {
            "theme": "DarkAmber"
        }
        with open("config.ini", "w") as config_file:
            cfg.write(config_file)
    return cfg


def get_default_ui_values(template_file: str = "ui_defaults.ini") -> dict:
    """ Read the configuration file for the default UI values.

    :return: The default values for the UI elements.
    """
    cfg = ConfigParser()
    cfg.read(template_file)
    cfg_dict = {}
    for section in cfg.sections():
        prefix = f"{section.lower()}_"
        for item in list(cfg[section].keys()):
            if section == "BUFFET_BIOMES":
                cfg_dict[prefix + item] = cfg.getboolean(section, item) or False
            elif section == "GAMERULES":
                try:
                    cfg_dict[prefix + item] = cfg.getboolean(section, item) or 0
                except ValueError:
                    cfg_dict[prefix + item] = cfg.getint(section, item) or 0
            else:
                cfg_dict[prefix + item] = cfg.get(section, item) or ""

    versions = cfg.getboolean("MAIN", "installed_versions")
    cfg_dict["main_installed_versions"] = versions
    cfg_dict["main_all_versions"] = not versions

    weather = cfg.get("MAIN", "weather")
    cfg_dict["main_rain"] = weather.lower() in ["rain", "raining"]
    cfg_dict["main_thundering"] = weather.lower() in ["thunder", "thundering"]
    cfg_dict["main_clear"] = not (
            cfg_dict["main_rain"] or cfg_dict["main_thundering"])

    cfg_dict["buffet_fluid_lava"] = (cfg_dict["buffet_fluid"] == "lava")
    cfg_dict["buffet_fluid_water"] = not cfg_dict["buffet_fluid_lava"]

    return cfg_dict


def set_default_ui_values(ui_values: dict,
                          template_file: str = "ui_defaults.ini") -> None:
    cfg = ConfigParser()
    sections = ["MAIN", "GAMERULES", "TERRAIN", "BUFFET", "BUFFET_BIOMES",
                "FLAT", "BORDER"]
    for s in sections:
        cfg.add_section(s)
    for k in ui_values:
        section = str(k).split("_")[0].upper()
        if section == "BUFFET" and "buffet_biomes" in k:
            section = "BUFFET_BIOMES"
        if section not in sections:
            continue

        key = k[len(section) + 1:]
        val = ui_values.get(k)
        if key == "name":
            continue
        if key in ["clear", "rain", "thundering"]:
            if val:
                cfg.set("MAIN", "weather", str(key))
            continue
        elif key in ["installed_versions", "all_versions"]:
            cfg.set("MAIN", "installed_versions",
                    str(key == "installed_versions" and val))
            continue
        elif key in ["fluid_lava", "fluid_water"]:
            if val:
                cfg.set("BUFFET", "fluid", str(key[len("fluid_"):]))
            continue

        cfg.set(section, key, str(val))
    with open(template_file, "w") as f:
        cfg.write(f, True)


@lru_cache(maxsize=4)
def find_installed_minecraft_versions(mc_dir: str = None) -> Dict:
    """ Finds the available jars of vanilla Minecraft in the system.

    Looks up the supported Jar files stored in mc_dir/versions folder and stores
    their name (e.g. '1.15.2') and path in a dictionary. The list of supported
    versions are obtained from the data version map, so not every Jar file in
    the path will be added to the dictionary.

    The method caches the result to prevent system lookups every time it is
    called.

    :param mc_dir: The Minecraft installation directory (.minecraft)
    :return: A dictionary containing the installed (and supported) minecraft
        versions and the path to the Jar files."""
    logging.info("Looking for installed minecraft versions")
    if not mc_dir:
        mc_dir = MC_FOLDER
    installations_folder = f"{mc_dir}/versions"
    installations = os.listdir(installations_folder)

    installed_versions = dict()
    for i in installations:
        if i in mu.version_map.keys():
            version_folder = f"{installations_folder}/{i}"
            if os.path.isdir(version_folder):
                version_jar = f"{version_folder}/{i}.jar"
                if os.path.isfile(version_jar):
                    installed_versions[str(i)] = str(version_jar)
    logging.info(f"Found {len(installed_versions)} installed version(s)")
    if not installed_versions:
        logging.warning("There are no installed Minecraft versions")
    return installed_versions


def change_directory(to_dir: str) -> str:
    """ Change to a different directory. Returns current directory.

    :param to_dir: The directory to change to.
    :return: The execution directory before changing directory. """
    logging.debug(f"Changing to directory {to_dir}")
    owd = os.getcwd()
    os.chdir(to_dir)
    return owd


def get_available_datapacks() -> List[
    Union[RandomLootDataPack, ExternalDatapack]]:
    """ Get a list of the datapacks that can be added to a world.

    Reads the zip files available in the assets/datapacks folder and
    creates an ExternalDatapack object with their path and name. The external
    datapacks are then appended after a RandomLootDatapack object, which is
    built during program runtime.

    :return: A list of the available datapacks.
    """
    datapacks = [RandomLootDataPack()]
    external_datapack_folder = f"{os.getcwd()}/assets/datapacks"
    for z in os.listdir(external_datapack_folder):
        if z.endswith(".zip"):
            dp = ExternalDatapack(f"{external_datapack_folder}/{z}")
            datapacks.append(dp)
    logging.info(f"Found {len(datapacks)} available datapacks")
    return datapacks
