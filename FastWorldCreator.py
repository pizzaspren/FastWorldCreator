import logging
from enum import Enum
from functools import partial
from typing import List, Type, Generator, Union

import PySimpleGUI as sg

from fast_world_creator import core
from fast_world_creator.utils import common_utils as cu, minecraft_utils as mu
from fast_world_creator.utils.level_dat_utils import get_default_gamerules

from fast_world_creator.ui import window

config = cu.get_or_create_config()
ui_defaults = cu.get_default_ui_values(config.get("UI", "template_file"))

log_format = "[%(asctime)s] [%(levelname)s] %(module)s - %(message)s"
logging.basicConfig(filename=config.get("LOGGING", "file"), format=log_format,
                    level=logging.getLevelName(config.get("LOGGING", "level") or
                                               "INFO"))
logging.info("Initializing")

sg.theme(config.get("UI", "theme"))  # Add a touch of color
sg.SetOptions(
    input_elements_background_color='#E9E9E9',
    input_text_color="#000000"
)


def enum_to_cb_contents(cls: Type[Enum]) -> List[str]:
    """ Extract enum.Enum names into a list, formatted as titles.

    :param cls: The Enum class to extract
    :return: The extracted names for the members of the enum
    """
    return [e.name.title() for e in cls]


available_datapacks = cu.get_available_datapacks()
available_datapacks.sort(key=lambda x: x.name)
difficulties = enum_to_cb_contents(mu.Difficulties)
game_modes = enum_to_cb_contents(mu.GameModes)
biomes = mu.get_mc_definitions("biomes")
gamerules = get_default_gamerules()


def parse_generator_options(values: dict) -> dict:
    """ Extract terrain generator options into a semi-parsed dictionary.

    :param values: The values generated from the PySimpleGUI window event."""

    def parse_flat_layers():
        layers = []
        for layer in values.get("flat_layers").split(","):
            if "*" in layer:
                layers.append(layer.split("*"))
            else:
                layers.append((1, layer))
        return layers

    logging.info("Parsing terrain generation options")
    return {
        "buffet_biome_type": values.get("buffet_biome_type").lower(),
        "buffet_biomes": [b for b in biomes if values[f"buffet_biomes_{b}"]],
        "buffet_size": int(values.get("buffet_size")),
        "buffet_block": values.get('buffet_block'),
        "buffet_fluid": "water" if values.get('buffet_fluid_water') else "lava",
        "buffet_chunk_type": values.get("buffet_chunk_type").lower(),

        "flat_biome": values.get('flat_biome'),
        "flat_layers": parse_flat_layers(),
        "flat_structures": dict.fromkeys(
            values.get("flat_structures").split(","))
    }


def parse_border_options(values: dict) -> dict:
    """ Extract the world border options from the values dictionary.

    :param values: The values generated from the PySimpleGUI window event.
    :return: The border options.
    """
    logging.info("Extracting world border options")
    border_opts = {}
    for k in list(values.keys()):
        if str(k).startswith("border_"):
            border_opts[k[len("border_"):]] = values.get(k)
    return border_opts


def create(values: dict) -> Generator[Union[str, int], None, None]:
    """ Start the creation of the Minecraft world and update the progress bar.

    :param values: The values generated from the PySimpleGUI window event."""
    logging.info("Preparing core execution")
    updated_gamerules = dict()
    for gr in gamerules:
        # Gamerules always stored as strings in level.dat
        updated_gamerules[gr] = str(values.get(f"gamerules_{gr}")).lower()
    parse_border_options(values)
    enabled_dp = [dp for dp in available_datapacks if values.get(dp.name, None)]

    execution = partial(
        core.run,
        version=values.get("main_release"),
        world_name=values.get("main_name").replace(" ", "_"),
        seed=values.get("main_seed"),
        difficulty=difficulties.index(values.get("main_difficulty")),
        datapacks=enabled_dp,
        gamerules=updated_gamerules,
        game_mode=game_modes.index(values.get("main_game_mode")),
        generator=values.get("terrain_generator").lower(),
        generator_options=parse_generator_options(values),
        raining=values.get("main_rain"),
        thundering=values.get("main_thunder"),
        border_settings=parse_border_options(values)
    )
    yield "start"
    # World folder, datapacks and level.dat
    total_yields = len(enabled_dp) + 2
    yield_counter = 0
    for _ in execution():
        yield_counter += 1
        yield yield_counter / total_yields * 100
    yield 100
    yield "done"


window = window.FwcWindow(title='Fast world creator', icon="assets/logo64.ico")
window.create_layouts(game_modes, difficulties, available_datapacks, gamerules,
                      biomes).finalize()

while True:
    event, val_dict = window.read(1000)
    if event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break
    elif event == "Ok":
        for status in create(val_dict):
            window.read(timeout=20)
            if status == "start":
                logging.info("Starting execution")
                window["progress_bar"].update(visible=True)
                window["progress_bar"].UpdateBar(0)
            elif status == "done":
                logging.info("Execution finished successfully")
                window["progress_bar"].update(visible=False)
            else:
                window["progress_bar"].UpdateBar(status)
    else:
        window.parse_events(event, val_dict)

window.close()
