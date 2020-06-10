import logging
import os
from configparser import ConfigParser
from functools import lru_cache
from typing import Dict, Type

import PySimpleGUI as sg

from fast_world_creator.utils import minecraft_utils as mu

MC_FOLDER = f"{os.getenv('APPDATA')}/.minecraft"


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


def ui_from_key(cls: Type[sg.Element], key: str, fallback: object,
                ui_defaults: dict, **kwargs: dict) -> sg.Element:
    """ Create a PySimpleGUI widget with the default value in a dict.

    :param cls: The class of the widget.
    :param key: The key to assign the widget.
    :param fallback: The default value if the key is not found in the dict.
    :param ui_defaults: The dict to extract the default value from.
    :param kwargs: Other arguments for the widget
    :return: The instantiated PySimpleGUI widget.
    """
    default_val = ui_defaults.get(key, fallback)
    if cls in [sg.Combo, sg.Slider]:
        return cls(default_value=default_val, key=key, **kwargs)
    if cls == sg.I:
        return cls(default_text=default_val, key=key, **kwargs)
    if cls == sg.Spin:
        return cls(initial_value=default_val, key=key, **kwargs)

    return cls(default=default_val, key=key, **kwargs)


def get_default_ui_values() -> dict:
    """ Read the configuration file for the default UI values.

    :return: The default values for the UI elements.
    """
    cfg = ConfigParser()
    cfg.read('defaults.ini')
    cfg_dict = {}
    for section in cfg.sections():
        prefix = f"{section.lower()}_" if section in ["BUFFET", "BUFFET_BIOME",
                                                      "FLAT", "BORDER"] else ""
        for item in list(cfg[section].keys()):
            if section == "BUFFET_BIOME":
                cfg_dict[prefix + item] = cfg.getboolean(section, item) or False
            else:
                cfg_dict[prefix + item] = cfg.get(section, item) or ""

    versions = cfg.getboolean("MAIN", "installed_versions")
    cfg_dict["radio_installed_versions"] = versions
    cfg_dict["radio_all_versions"] = not versions

    weather = cfg.get("MAIN", "weather")
    cfg_dict["rain"] = weather.lower() in ["rain", "raining"]
    cfg_dict["thundering"] = weather.lower() in ["thunder", "thundering"]
    cfg_dict["clear"] = not (cfg_dict["rain"] or cfg_dict["thundering"])

    cfg_dict["buffet_fluid_lava"] = (cfg_dict["buffet_fluid"] == "lava")
    cfg_dict["buffet_fluid_water"] = not cfg_dict["buffet_fluid_lava"]

    return cfg_dict


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
