import os
import sys
from typing import Dict

from fast_world_creator.utils import version_mapping


def log(msg: str, sym: str = "#") -> None:
    """ Log a formatted message. """
    print(f"{sym * 3} {msg:^40} {sym * 3}")


def find_installed_minecraft_versions(mc_dir: str = None) -> Dict:
    """ Finds the available jars of vanilla Minecraft in the system. """
    log("Looking for installed minecraft versions")
    if not mc_dir:
        mc_dir = get_mc_folder()
    installations_folder = os.sep.join([mc_dir, "versions"])
    installations = os.listdir(installations_folder)

    installed_versions = dict()
    for i in installations:
        if i in version_mapping.version_map.keys():
            version_folder = os.sep.join([installations_folder, i])
            if os.path.isdir(version_folder):
                version_jar = os.sep.join([version_folder, i]) + ".jar"
                if os.path.isfile(version_jar):
                    installed_versions[str(i)] = str(version_jar)
    log(f"Found {len(installed_versions)} installed version(s)")
    if not installed_versions:
        log("Aborting...")
        exit(0)
    return installed_versions


def get_mc_folder():
    if not get_mc_folder.loaded:
        get_mc_folder.loaded = os.sep.join([os.getenv("APPDATA"), ".minecraft"])
    return get_mc_folder.loaded


get_mc_folder.loaded = False


def pick_minecraft_version(versions: Dict) -> str:
    """ Has the user select a Minecraft version from the installed versions."""
    log("Select the Minecraft version you want to play in:", sym="-")
    for k in versions.keys():
        print(f"  -> {k:<6}")
    selection = input("> ")
    return selection


def change_directory(to_dir: str) -> str:
    """ Change to a different directory. Returns current directory. """
    owd = os.getcwd()
    os.chdir(to_dir)
    return owd


def parse_cmd_arguments() -> Dict:
    """ Parse the command line arguments and store them into a dictionary. """
    arg_dict = {}
    for arg in sys.argv[1:]:
        arg_k, arg_v = arg.split("=")
        arg_dict[f"arg_{arg_k}"] = arg_v
    return arg_dict
