import os
from typing import Dict

from fast_world_creator.utils import minecraft_utils as mu


def log(msg: str, sym: str = "#") -> None:
    """ Log a formatted message.

    :param msg: The message to log.
    :param sym: The symbol to use for flair.
    """
    print(f"{sym * 3} {msg:^40} {sym * 3}")


def find_installed_minecraft_versions(mc_dir: str = None) -> Dict:
    """ Finds the available jars of vanilla Minecraft in the system.

    Looks up the supported Jar files stored in mc_dir/versions folder and stores
    their name (e.g. '1.15.2') and path in a dictionary. The list of supported
    versions are obtained from the data version map, so not every Jar file in
    the path will be added to the dictionary.

    :param mc_dir: The Minecraft installation directory (.minecraft)
    :return: A dictionary containing the installed (and supported) minecraft
        versions and the path to the Jar files."""
    log("Looking for installed minecraft versions")
    if not mc_dir:
        mc_dir = get_mc_folder()
    installations_folder = f"{mc_dir}/versions"
    installations = os.listdir(installations_folder)

    installed_versions = dict()
    for i in installations:
        if i in mu.get_version_map().keys():
            version_folder = f"{installations_folder}/{i}"
            if os.path.isdir(version_folder):
                version_jar = f"{version_folder}/{i}.jar"
                if os.path.isfile(version_jar):
                    installed_versions[str(i)] = str(version_jar)
    log(f"Found {len(installed_versions)} installed version(s)")
    if not installed_versions:
        log("Aborting...")
        exit(0)
    return installed_versions


def get_mc_folder() -> str:
    """ Get the default Minecraft installation folder

    The method caches the result to prevent system lookups every time it is
    called.
    :return: The path to the folder.
    """
    if not get_mc_folder.loaded_version:
        get_mc_folder.loaded_version = f"{os.getenv('APPDATA')}/.minecraft"
    return get_mc_folder.loaded_version


# Manual cache for the get_mc_folder method
get_mc_folder.loaded_version = False


def change_directory(to_dir: str) -> str:
    """ Change to a different directory. Returns current directory.

    :param to_dir: The directory to change to.
    :return: The execution directory before changing directory. """
    owd = os.getcwd()
    os.chdir(to_dir)
    return owd
