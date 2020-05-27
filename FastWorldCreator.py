import PySimpleGUI as sg

from fast_world_creator import core
from fast_world_creator.utils import common_utils as cu
from fast_world_creator.utils import datapack_utils as du
from fast_world_creator.utils import minecraft_utils as mu
from fast_world_creator.utils.level_dat_utils import get_default_gamerules

sg.theme('DarkAmber')  # Add a touch of color
sg.SetOptions(
    input_elements_background_color='#E9E9E9',
    input_text_color="#000000"
)


def enum_to_cb_contents(cls):
    return [e.name.title() for e in cls]


installed_versions = cu.find_installed_minecraft_versions()
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
    def create_main_tab_layout():
        c1_layout = [[
            sg.T('MC Version', size=(10, 1)),
            sg.Combo(
                [k for k in installed_versions.keys()],
                default_value=list(installed_versions.keys())[-1],
                size=(18, 1),
                readonly=True,
                key="release")
        ]]
        c1_layout += [[
            sg.T('World Name', size=(10, 1)),
            sg.I(size=(20, 1), key="name")
        ]]
        c1_layout += [[
            sg.T('Seed', size=(10, 1), tooltip="Leave blank for random seed"),
            sg.I(size=(20, 1), tooltip="Leave blank for random seed",
                 key="seed")
        ]]
        c1_layout += [[
            sg.T('Difficulty', size=(10, 1)),
            sg.Combo(difficulties, difficulties[0], (18, 1), readonly=True,
                     key="difficulty")
        ]]
        c1_layout += [[
            sg.T('Game mode', size=(10, 1)),
            sg.Combo(game_modes, game_modes[0], (18, 1), readonly=True,
                     key="game_mode")
        ]]
        c2_layout = [[sg.Frame('Weather', create_weather_layout())]]
        layout = [[
            sg.Col(c1_layout, pad=(5, 7)), sg.Col(c2_layout, pad=(0, 17))
        ]]
        layout += [[
            sg.Frame('Datapacks', create_datapack_layout(), size=(50, 1))
        ]]
        return layout

    def create_weather_layout():
        layout = [
            [sg.Radio("Clear", "weather", True)],
            [sg.Radio("Rain", "weather", key="rain")],
            [sg.CB("Thunder", key="thundering")]
        ]
        return layout

    def create_datapack_layout():
        grouped_packs = [
            available_datapacks[i:i + 2] for i in
            range(0, len(available_datapacks), 2)
        ]
        c1_layout, c2_layout = sg.Sizer(20, 1), sg.Sizer(20, 1)
        for d_pair in grouped_packs:
            for d, c in zip(d_pair, [c1_layout, c2_layout]):
                c.add_row(sg.CB(d.name, d.default_enabled, (15, 1),
                                tooltip=f"{d.name}\n{d.description}",
                                key=d.name))
        return [[c1_layout, c2_layout]]

    def create_gamerule_layout():
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

    tab1 = sg.Tab("Main", create_main_tab_layout())
    tab2 = sg.Tab("Gamerules", create_gamerule_layout())
    tab3 = sg.Tab("Terrain", create_terrain_layout())
    main_layout = [
        [sg.TabGroup([[tab1, tab2, tab3]])],
        [sg.Button('Ok'), sg.Button('Cancel')]
    ]
    return main_layout


def parse_generator_options(values):
    def parse_flat_layers():
        layers = []
        for layer in values.get("flat_layers").split(","):
            if "*" in layer:
                layers.append(layer.split("*"))
            else:
                layers.append((1, layer))
        return layers

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


def create(values: dict) -> None:
    updated_gamerules = dict()
    for gr in gamerules:
        # Gamerules always stored as strings
        updated_gamerules[gr] = str(values.get(gr)).lower()
    core.run(
        version_pair=(
            values.get("release"),
            installed_versions[values.get("release")]
        ),
        world_name=values.get("name").replace(" ", "_"),
        seed=values.get("seed"),
        difficulty=difficulties.index(values.get("difficulty")),
        datapacks=[dp for dp in available_datapacks if values[dp.name]],
        gamerules=updated_gamerules,
        game_mode=game_modes.index(values.get("game_mode")),
        generator=values.get("generator").lower(),
        generator_options=parse_generator_options(values),
        raining=values.get("rain"),
        thundering=values.get("thunder")
    )


window = sg.Window(
    title='Fast world creator',
    layout=create_layouts(),
    icon="assets/logo64.ico",
    finalize=True)
window["buffet_option_frame"].hide_row()
window["flat_option_frame"].hide_row()
window["buffet_size"].hide_row()

while True:
    event, val_dict = window.read()
    if event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break
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
        create(val_dict)
        break

window.close()
