from __future__ import annotations

import logging

import PySimpleGUI as sg

from fast_world_creator.utils import common_utils as cu, minecraft_utils as mu

supported_versions = [k for k in mu.version_map]
installed_versions = [k for k in cu.find_installed_minecraft_versions()]
installed_versions.sort(reverse=True)
generators = mu.generator_names
generators.sort()
superflat_presets = [p.split(";") for p in
                     mu.get_mc_definitions("superflat_presets")]
superflat_dict = {preset[0]: preset[1:] for preset in superflat_presets}
SF_BLOCK, SF_BIOME, SF_STRUCT = range(0, 3)


class FwcWindow(sg.Window):

    def __init__(self, *args, **kwargs):
        super(FwcWindow, self).__init__(*args, **kwargs)

    def parse_events(self, event: str, val_dict: dict) -> None:
        if event == "main_installed_versions":
            self["main_release"].update(values=installed_versions)
        elif event == "main_all_versions":
            self["main_release"].update(values=supported_versions)
        elif event == "terrain_generator":
            if val_dict[event] == "Buffet":
                self["buffet_option_frame"].unhide_row()
            else:
                self["buffet_option_frame"].hide_row()
            if val_dict[event] == "Flat":
                self["flat_option_frame"].unhide_row()
            else:
                self["flat_option_frame"].hide_row()
        elif event == "buffet_biome_type":
            if val_dict[event] == "Vanilla_layered":
                self["buffet_biomes"].hide_row()
            else:
                self["buffet_biomes"].unhide_row()
            if val_dict[event] == "Checkerboard":
                self["buffet_size"].unhide_row()
            else:
                self["buffet_size"].hide_row()
        elif event == "flat_preset":
            self["flat_biome"].update(
                value=superflat_dict[val_dict[event]][SF_BIOME])
            self["flat_layers"].update(
                value=superflat_dict[val_dict[event]][SF_BLOCK])
            self["flat_structures"].update(
                value=superflat_dict[val_dict[event]][SF_STRUCT])

    def create_layouts(self, game_modes, difficulties, datapacks, gamerules,
                       biomes) -> FwcWindow:
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
                        sg.Combo(installed_versions, installed_versions[0],
                                 (25, 1), readonly=True, key="main_release")
                    ],
                    [
                        sg.Radio("Show installed versions", "radio_versions",
                                 True, enable_events=True,
                                 key="main_installed_versions"),
                        sg.Radio("Show all versions", "radio_versions",
                                 False, enable_events=True,
                                 key="main_all_versions")
                    ]
                ])
            ]]
            c1_layout = [[
                sg.T('World Name', size=(10, 1)),
                sg.I(size=(21, 1), key="main_name")
            ]]
            c1_layout += [[
                sg.T('Seed', size=(10, 1),
                     tooltip="Leave blank for random seed"),
                sg.I("", (21, 1), tooltip="Leave blank for random seed",
                     key="main_seed")
            ]]
            c1_layout += [[
                sg.T('Difficulty', size=(10, 1)),
                sg.Combo(difficulties, difficulties[0], (19, 1), readonly=True,
                         key="main_difficulty")
            ]]
            c1_layout += [[
                sg.T('Game mode', size=(10, 1)),
                sg.Combo(game_modes, game_modes[0], (19, 1), readonly=True,
                         key="main_game_mode")
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
                [sg.Radio("Clear", "weather", True, key="main_clear")],
                [sg.Radio("Rain", "weather", False, key="main_rain")],
                [sg.Radio("Thunder", "weather", False, key="main_thundering")]
            ]
            return layout

        def create_datapack_layout():
            """Create layout for the datapack frame.

            Groups all the available datapacks in two columns. Each datapack can
            be selected with a Checkbox, which has a default state equal to the
            datapack's 'default_enabled' field.
            """
            logging.debug("Creating datapack layout")
            grouped_packs = [
                datapacks[i:i + 2] for i in
                range(0, len(datapacks), 2)
            ]
            logging.debug(f"Found {len(grouped_packs)} pairs of datapacks")
            c1_layout, c2_layout = sg.Sizer(20, 1), sg.Sizer(20, 1)
            for d_pair in grouped_packs:
                for d, c in zip(d_pair, [c1_layout, c2_layout]):
                    c.add_row(sg.CB(d.name, d.default_enabled, (15, 1),
                                    tooltip=f"{d.name}\n{d.description}"))
            return [
                [c1_layout, c2_layout],
                [sg.T("_"*35, (41, 0),
                      justification="center", pad=(2, 0))],
                [sg.T("Drop your datapacks in 'assets/datapacks'", (41, 0),
                      justification="center", pad=(2, 0))]
            ]

        def create_gamerule_layout():
            """Create layout for the gamerules tab.

            Contains all the gamerules available for the game, grouped into a
            single column. The gamerules with a boolean value are assigned a
            CheckBox, and the gamerules with an integer value are assigned an
            Input element
            """
            logging.debug("Creating gamerule layout")
            grouped = sg.Column([[]], scrollable=True,
                                vertical_scroll_only=True)
            for gr in gamerules.keys():
                col1, col2 = sg.Sizer(20, 1), sg.Sizer(15, 1)
                col2.ElementJustification = "right"
                col1.add_row(sg.Text(gr, (25, 1)))
                key = f"gamerules_{gr}"
                if isinstance(gamerules.get(gr), bool):
                    col2.add_row(sg.CB("", gamerules.get(gr), key=key))
                else:
                    col2.add_row(sg.I(gamerules.get(gr), (10, 1), key=key))
                grouped.add_row(col1, col2)
            return [[grouped]]

        def create_terrain_layout():
            """Create layout for the terrain tab.

            Contains all the options for the different terrain generators
            available in the game (1.13 until pre-20w21a).
            """
            logging.debug("Creating terrain layout")
            layout = []
            layout += [[
                sg.T("World type", (16, 1), pad=(10, 10)),
                sg.Combo(generators, "Default", (25, 1), pad=(3, 10),
                         readonly=True, enable_events=True,
                         key="terrain_generator")
            ]]
            layout += [[sg.Frame('Buffet options', create_buffet_options(),
                                 key='buffet_option_frame')]]
            layout += [
                [sg.Frame('Superflat options', create_superflat_options(),
                          key='flat_option_frame')]]
            return layout

        def create_buffet_options():
            """Create layout for the buffet frame.

            Being the most complex generator in the game, the buffet terrain
            generator offers a lot of customization options. The data is pulled
            from the assets folder and put into fields that can be easily
            differentiated by the users.
            """
            logging.debug("Creating buffet layout")
            layout = [[
                sg.T("Chunk generator", (15, 1)),
                sg.Combo(mu.buffet_chunk_gen, mu.buffet_chunk_gen[0], (25, 1),
                         readonly=True, enable_events=True,
                         key="buffet_chunk_type")
            ]]
            layout += [[
                sg.T("Default block", (15, 1)),
                sg.Combo(mu.get_mc_definitions("blocks"), "stone", (25, 1),
                         key="buffet_block")
            ]]
            layout += [[
                sg.T("Default fluid", (15, 1)),
                sg.Radio("Water", "buffet_fluid", True,
                         key="buffet_fluid_water"),
                sg.Radio("Lava", "buffet_fluid", False,
                         key="buffet_fluid_lava"),
            ]]
            layout += [[sg.Text("┈" * 46)]]
            layout += [[
                sg.T("Biomes distribution", (15, 1)),
                sg.Combo(mu.buffet_types, mu.buffet_types[0], (25, 1),
                         readonly=True, enable_events=True,
                         key="buffet_biome_type")
            ]]
            layout += [[
                sg.T("Checkerboard size", (15, 1)),
                sg.Slider((-4, 16), 2, orientation='h', tooltip="".join([
                    "The biome squares will have sides of 2^size chunks.",
                    "\n -4 = 1 block\n 16 = 65536 chunks"]), key="buffet_size")
            ]]
            layout += [[
                sg.T("Biomes", (15, 1)),
                sg.Col([
                    [sg.CB(b, False, key=f"buffet_biomes_{b}")] for b in
                    biomes], size=(175, 125), pad=(5, 5), scrollable=True,
                    vertical_scroll_only=True, key="buffet_biomes")
            ]]
            return layout

        def create_superflat_options():
            """Create layout for the superflat frame.

            The data is pulled from the assets folder and put into fields that
            can be easily differentiated by the users.
            """
            logging.debug("Creating superflat layout")
            layout = []
            layout += [[
                sg.T("Presets", (15, 1)),
                sg.Combo(list(superflat_dict.keys()), superflat_presets[0][0],
                         (25, 1), readonly=True, enable_events=True,
                         key="flat_preset")
            ]]
            layout += [[
                sg.T("Biome", (15, 1)),
                sg.Combo(biomes, superflat_presets[0][2], (25, 1),
                         readonly=True, key="flat_biome")
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
                    sg.T("Z"), sg.I("0", (19, 1), key="border_z")
                ]])
            ]]
            col1_layout = [[
                sg.Frame("Border size", [
                    [
                        sg.T("Initial size", (8, 1)),
                        sg.I("60000000", (10, 1), key="border_size",
                             justification="right")
                    ],
                    [
                        sg.T("Final size", (8, 1)),
                        sg.I("60000000", (10, 1), key="border_size_target",
                             justification="right")
                    ],
                    [
                        sg.T("Lerp time", (8, 1),
                             tooltip="Seconds until border reaches final size"),
                        sg.I("0", (10, 1), key="border_lerp_time",
                             justification="right")
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
                sg.I("5", (8, 1), key="border_safe_blocks",
                     justification="right")
            ]]
            col2_layout += [[
                sg.T("Warning time", (11, 1)),
                sg.I("15", (8, 1), key="border_warn_time",
                     justification="right")
            ]]
            col2_layout += [[
                sg.T("Warning blocks", (11, 1)),
                sg.I("5", (8, 1), key="border_warn_blocks",
                     justification="right")
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
                sg.B("Create", button_color=("white", "green")),
                sg.B("Quit", button_color=("white", "red")),
                sg.ProgressBar(100, "horizontal", (13, 23),
                               bar_color=("#FDCB52", "#2C2825"),
                               key="progress_bar"),
                sg.B("Save", tooltip="Save values to template"),
                sg.B("Load", tooltip="Load values from template"),
            ]
        ]
        self.layout(main_layout)
        return self

    def Finalize(self):
        super(FwcWindow, self).Finalize()
        self["border_damage"].Widget.configure(justify="right")
        self.update_element_visibility()

    finalize = Finalize

    def set_values_from_dict(self, key_dict: dict = None) -> None:
        if not key_dict:
            return
        for key in key_dict.keys():
            if key in self.AllKeysDict:
                self[key].update(key_dict.get(key))
        self.update_element_visibility()

    def update_element_visibility(self):
        if self["terrain_generator"].get() != "Buffet":
            self["buffet_option_frame"].hide_row()
        if self["terrain_generator"].get() != "Flat":
            self["flat_option_frame"].hide_row()
        if self["buffet_biome_type"].get() != "Checkerboard":
            self["buffet_size"].hide_row()
        if self["main_all_versions"].get():
            self["main_release"].update(values=supported_versions,
                                        value=self["main_release"].get())
        else:
            self["main_release"].update(values=installed_versions,
                                        value=self["main_release"].get())
