import logging
from enum import Enum
from functools import partial
from typing import List, Type, Generator, Union

import PySimpleGUI as sg

from fast_world_creator import core
from fast_world_creator.utils import common_utils as cu
from fast_world_creator.utils import datapack_utils as du
from fast_world_creator.utils import minecraft_utils as mu
from fast_world_creator.utils.level_dat_utils import get_default_gamerules

config = cu.get_or_create_config()

log_format = "[%(asctime)s] [%(levelname)s] %(module)s - %(message)s"
logging.basicConfig(filename=config.get("LOGGING", "file"),
                    format=log_format,
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


supported_mc_versions = [k for k in mu.version_map]
installed_mc_versions = [k for k in cu.find_installed_minecraft_versions()]
installed_mc_versions.sort(reverse=True)
available_datapacks = du.get_available_datapacks()
available_datapacks.sort(key=lambda x: x.name)
difficulties = enum_to_cb_contents(mu.Difficulties)
game_modes = enum_to_cb_contents(mu.GameModes)
generators = enum_to_cb_contents(mu.GeneratorNames)
generators.sort()
buffet_biome_types = enum_to_cb_contents(mu.BuffetOpts.BType)
chunk_generator_types = enum_to_cb_contents(mu.BuffetOpts.BChunkGen)
biomes = mu.get_mc_definitions("biomes")
blocks = mu.get_mc_definitions("blocks")
superflat_presets = [p.split(";") for p in
                     mu.get_mc_definitions("superflat_presets")]
superflat_dict = dict()
for preset in superflat_presets:
    superflat_dict[preset[0]] = preset[1:]
SF_BLOCK, SF_BIOME, SF_STRUCT = range(0, 3)
gamerules = get_default_gamerules()


def create_layouts():
    """Create all the layouts for the GUI window."""

    def create_main_tab_layout():
        """Create layout for the main tab.

        Contains most common Minecraft options such as version, world name,
        seed, game mode and difficulty. Datapack selection is bundled in the
        main tab, and populated from the assets/datapacks folder.
        """
        logging.debug("Creating main tab layout")
        layout = [[
            sg.Frame("Version", [
                [
                    sg.T('Minecraft Version', size=(15, 1)),
                    sg.Combo(installed_mc_versions, installed_mc_versions[0],
                             (25, 1), readonly=True, key="release")
                ],
                [
                    sg.Radio("Show installed versions", "radio_versions", True,
                             enable_events=True,
                             key="radio_installed_versions"),
                    sg.Radio("Show all versions", "radio_versions",
                             enable_events=True, key="radio_all_versions")
                ]
            ])
        ]]
        c1_layout = [[
            sg.T('World Name', size=(10, 1)),
            sg.I(size=(21, 1), key="name")
        ]]
        c1_layout += [[
            sg.T('Seed', size=(10, 1), tooltip="Leave blank for random seed"),
            sg.I(size=(21, 1), tooltip="Leave blank for random seed",
                 key="seed")
        ]]
        c1_layout += [[
            sg.T('Difficulty', size=(10, 1)),
            sg.Combo(difficulties, difficulties[0], (19, 1), readonly=True,
                     key="difficulty")
        ]]
        c1_layout += [[
            sg.T('Game mode', size=(10, 1)),
            sg.Combo(game_modes, game_modes[0], (19, 1), readonly=True,
                     key="game_mode")
        ]]
        c2_layout = [[sg.Frame('Weather', create_weather_layout())]]
        layout += [[
            sg.Col(c1_layout, pad=(0, 5)), sg.Col(c2_layout, pad=(0, 0))
        ]]
        layout += [[
            sg.Frame('Datapacks', create_datapack_layout(), size=(50, 1))
        ]]
        return layout

    def create_weather_layout():
        """Create layout for the weather frame.

        Contains selection for rain/clear/thundering weather.
        """
        logging.debug("Creating weather layout")
        layout = [
            [sg.Radio("Clear", "weather", True)],
            [sg.Radio("Rain", "weather", key="rain")],
            [sg.Radio("Thunder", "weather", key="thundering")]
        ]
        return layout

    def create_datapack_layout():
        """Create layout for the datapack frame.

        Groups all the available datapacks in two columns. Each datapack can be
        selected with a Checkbox, which has a default state equal to the
        datapack's 'default_enabled' field.
        """
        logging.debug("Creating datapack layout")
        grouped_packs = [
            available_datapacks[i:i + 2] for i in
            range(0, len(available_datapacks), 2)
        ]
        logging.debug(f"Found {len(grouped_packs)} pairs of datapacks")
        c1_layout, c2_layout = sg.Sizer(20, 1), sg.Sizer(20, 1)
        for d_pair in grouped_packs:
            for d, c in zip(d_pair, [c1_layout, c2_layout]):
                c.add_row(sg.CB(d.name, d.default_enabled, (15, 1),
                                tooltip=f"{d.name}\n{d.description}",
                                key=d.name))
        return [[c1_layout, c2_layout]]

    def create_gamerule_layout():
        """Create layout for the gamerules tab.

        Contains all the gamerules available for the game, grouped into a single
        column. The gamerules with a boolean value are assigned a CheckBox, and
        the gamerules with an integer value are assigned an Input element
        """
        logging.debug("Creating gamerule layout")
        grouped = sg.Column([[]], scrollable=True, vertical_scroll_only=True)
        for gr in gamerules.keys():
            col1, col2 = sg.Sizer(20, 1), sg.Sizer(15, 1)
            col2.ElementJustification = "right"
            col1.add_row(
                sg.Text(gr, (25, 1))
            )
            if isinstance(gamerules.get(gr), bool):
                col2.add_row(sg.CB("", gamerules.get(gr), key=gr))
            else:
                col2.add_row(sg.I(gamerules.get(gr), (10, 1), key=gr))
            grouped.add_row(col1, col2)
        return [[grouped]]

    def create_terrain_layout():
        """Create layout for the terrain tab.

        Contains all the options for the different terrain generators available
        in the game (1.13 until pre-20w21a).
        """
        logging.debug("Creating terrain layout")
        layout = []
        layout += [[
            sg.T("World type", (16, 1), pad=(10, 10)),
            sg.Combo(generators, mu.GeneratorNames.DEFAULT.value.title(),
                     (25, 1), pad=(3, 10), readonly=True, enable_events=True,
                     key="generator")
        ]]
        layout += [[sg.Frame('Buffet options', create_buffet_options(),
                             key='buffet_option_frame')]]
        layout += [[sg.Frame('Superflat options', create_superflat_options(),
                             key='flat_option_frame')]]
        return layout

    def create_buffet_options():
        """Create layout for the buffet frame.

        Being the most complex generator in the game, the buffet terrain
        generator offers a lot of customization options. The data is pulled from
        the assets folder and put into fields that can be easily differentiated
        by the users.
        """
        logging.debug("Creating buffet layout")
        layout = [[
            sg.T("Chunk generator", (15, 1)),
            sg.Combo(chunk_generator_types, chunk_generator_types[0],
                     (25, 1), readonly=True, enable_events=True,
                     key="buffet_chunk_type")
        ]]
        layout += [[
            sg.T("Default block", (15, 1)),
            sg.Combo(blocks, "stone", (25, 1), key="buffet_block")
        ]]
        layout += [[
            sg.T("Default fluid", (15, 1)),
            sg.Radio("Water", "buffet_fluid", True, key="buffet_fluid"),
            sg.Radio("Lava", "buffet_fluid")
        ]]
        layout += [[sg.Text("┈" * 46)]]
        layout += [[
            sg.T("Biomes distribution", (15, 1)),
            sg.Combo(buffet_biome_types, buffet_biome_types[0], (25, 1),
                     readonly=True, enable_events=True, key="buffet_biome_type")
        ]]
        layout += [[
            sg.T("Checkerboard size", (15, 1)),
            sg.Slider((-4, 16), 2, orientation='h', tooltip="".join([
                "The biome squares will have sides of 2^size chunks.\n",
                "  -4 = 1 block\n  16 = 65536 chunks"]),
                      key="buffet_size")
        ]]
        layout += [[
            sg.T("Biomes", (15, 1)),
            sg.Col([[sg.CB(b, key=f"buffet_biome_{b}")] for b in biomes],
                   size=(175, 125), pad=(5, 5), scrollable=True,
                   vertical_scroll_only=True, key="buffet_biomes")
        ]]
        return layout

    def create_superflat_options():
        """Create layout for the superflat frame.

        The data is pulled from the assets folder and put into fields that can
        be easily differentiated by the users.
        """
        logging.debug("Creating superflat layout")
        layout = []
        layout += [[
            sg.T("Presets", (15, 1)),
            sg.Combo(list(superflat_dict.keys()), superflat_presets[0][0],
                     size=(25, 1), readonly=True, enable_events=True,
                     key="flat_preset")
        ]]
        layout += [[
            sg.T("Biome", (15, 1)),
            sg.Combo(biomes, superflat_presets[0][2], (25, 1), readonly=True,
                     key="flat_biome")
        ]]
        layout += [[
            sg.T("Layers", (15, 1)),
            sg.I(superflat_presets[0][1], (27, 1), key="flat_layers")
        ]]
        layout += [[
            sg.T("Structure flags", (15, 1)),
            sg.I(superflat_presets[0][3], (27, 1), key="flat_structures")
        ]]
        return layout

    def create_border_options():
        """Create layout for the world border tab.

        Contains all the available options for the modification of the world
        border.
        """
        logging.debug("Creating world border layout")
        layout = [[
            sg.Frame("Border center", [[
                sg.T("X"), sg.I("0", (19, 1), key="border_x"),
                sg.T("Z"), sg.I("0", (19, 1), key="border_z"),
            ]])
        ]]
        col1_layout = [[
            sg.Frame("Border size", [
                [
                    sg.T("Initial size", (8, 1)),
                    sg.I("60000000", (10, 1), justification="right",
                         key="border_size")
                ],
                [
                    sg.T("Final size", (8, 1)),
                    sg.I("60000000", (10, 1), justification="right",
                         key="border_size_target")
                ],
                [
                    sg.T("Lerp time", (8, 1),
                         tooltip="Seconds until border reaches final size"),
                    sg.I("0", (10, 1), justification="right",
                         key="border_lerp_time")
                ]
            ])
        ]]
        col2_layout = [[
            sg.T("Damage", (11, 1), tooltip="Damage per block"),
            sg.Spin([str(x / 10) for x in range(201)], "0.2", size=(7, 1),
                    key="border_damage")
        ]]
        col2_layout += [[
            sg.T("Safe distance", (11, 1), tooltip="Blocks beyond border"),
            sg.I("5", (8, 1), justification="right", key="border_safe_blocks")
        ]]
        col2_layout += [[
            sg.T("Warning time", (11, 1)),
            sg.I("15", (8, 1), justification="right", key="border_warn_time")
        ]]
        col2_layout += [[
            sg.T("Warning blocks", (11, 1)),
            sg.I("5", (8, 1), justification="right", key="border_warn_blocks")
        ]]
        layout += [[
            sg.Col(col2_layout, pad=(0, 0)),
            sg.Col(col1_layout, pad=(0, 0))
        ]]
        return layout

    logging.debug("Creating window tabs")
    tab1 = sg.Tab("Main", create_main_tab_layout())
    tab2 = sg.Tab("Gamerules", create_gamerule_layout())
    tab3 = sg.Tab("Terrain", create_terrain_layout())
    tab4 = sg.Tab("Border", create_border_options())
    main_layout = [
        [sg.TabGroup([[tab1, tab2, tab3, tab4]])],
        [
            sg.Button('Ok'), sg.Button('Cancel'),
            sg.T("", (4, 0)),
            sg.ProgressBar(100, "horizontal", (20, 23), key="progress_bar")
        ]
    ]
    return main_layout


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
        "buffet_biomes": [b for b in biomes if values[f"buffet_biome_{b}"]],
        "buffet_size": int(values.get("buffet_size")),
        "buffet_block": values.get('buffet_block'),
        "buffet_fluid": "water" if values.get('buffet_fluid') else "lava",
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
        # Gamerules always stored as strings
        updated_gamerules[gr] = str(values.get(gr)).lower()
    parse_border_options(values)
    enabled_dp = [dp for dp in available_datapacks if values[dp.name]]

    execution = partial(
        core.run,
        version=values.get("release"),
        world_name=values.get("name").replace(" ", "_"),
        seed=values.get("seed"),
        difficulty=difficulties.index(values.get("difficulty")),
        datapacks=enabled_dp,
        gamerules=updated_gamerules,
        game_mode=game_modes.index(values.get("game_mode")),
        generator=values.get("generator").lower(),
        generator_options=parse_generator_options(values),
        raining=values.get("rain"),
        thundering=values.get("thunder"),
        border_settings=parse_border_options(values)
    )
    yield "start"
    # World folder, datapacks, level.dat
    total_yields = len(enabled_dp) + 2
    yield_counter = 0
    for _ in execution():
        yield_counter += 1
        yield yield_counter / total_yields * 100
    yield 100
    yield "done"


window = sg.Window(
    title='Fast world creator',
    layout=create_layouts(),
    icon="assets/logo64.ico",
    finalize=True)
window["buffet_option_frame"].hide_row()
window["flat_option_frame"].hide_row()
window["buffet_size"].hide_row()
window["border_damage"].Widget.configure(justify="right")
window["progress_bar"].update(visible=False)

while True:
    event, val_dict = window.read(1000)
    if event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break
    if event == "radio_installed_versions":
        window["release"].update(values=installed_mc_versions)
    elif event == "radio_all_versions":
        window["release"].update(values=supported_mc_versions)
    if event == "generator":
        if val_dict[event] == mu.GeneratorNames.BUFFET.name.title():
            window["buffet_option_frame"].unhide_row()
        else:
            window["buffet_option_frame"].hide_row()
        if val_dict[event] == mu.GeneratorNames.FLAT.name.title():
            window["flat_option_frame"].unhide_row()
        else:
            window["flat_option_frame"].hide_row()
    elif event == "buffet_biome_type":
        if val_dict[event] == mu.BuffetOpts.BType.VANILLA_LAYERED.name.title():
            window["buffet_biomes"].hide_row()
        else:
            window["buffet_biomes"].unhide_row()
        if val_dict[event] == mu.BuffetOpts.BType.CHECKERBOARD.name.title():
            window["buffet_size"].unhide_row()
        else:
            window["buffet_size"].hide_row()
    elif event == "flat_preset":
        window["flat_biome"].update(
            value=superflat_dict[val_dict[event]][SF_BIOME])
        window["flat_layers"].update(
            value=superflat_dict[val_dict[event]][SF_BLOCK])
        window["flat_structures"].update(
            value=superflat_dict[val_dict[event]][SF_STRUCT])

    if event == "Ok":
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

window.close()
