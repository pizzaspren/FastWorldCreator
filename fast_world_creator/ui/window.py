from __future__ import annotations

import logging

import PySimpleGUI as sg

from fast_world_creator.ui import defaulted_elements as de
from fast_world_creator.utils import common_utils as cu, minecraft_utils as mu

config = cu.get_or_create_config()
ui_defaults = cu.get_default_ui_values()

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
                        de.DefaultedCombo(ui_defaults, "main_release",
                                          installed_versions,
                                          size=(25, 1), readonly=True)
                    ],
                    [
                        de.DefaultedRadio(ui_defaults,
                                          "main_installed_versions", True,
                                          text="Show installed versions",
                                          group_id="radio_versions",
                                          enable_events=True),
                        de.DefaultedRadio(ui_defaults,
                                          "main_all_versions", False,
                                          text="Show all versions",
                                          group_id="radio_versions",
                                          enable_events=True)
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
                de.DefaultedInput(ui_defaults, "main_seed", "", size=(21, 1),
                                  tooltip="Leave blank for random seed")
            ]]
            c1_layout += [[
                sg.T('Difficulty', size=(10, 1)),
                de.DefaultedCombo(ui_defaults, "main_difficulty", difficulties,
                                  size=(19, 1), readonly=True)
            ]]
            c1_layout += [[
                sg.T('Game mode', size=(10, 1)),
                de.DefaultedCombo(ui_defaults, "main_game_mode", game_modes,
                                  size=(19, 1), readonly=True)
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
                [de.DefaultedRadio(ui_defaults, "main_clear", True,
                                   text="Clear", group_id="weather")],
                [de.DefaultedRadio(ui_defaults, "main_rain", False, text="Rain",
                                   group_id="weather")],
                [de.DefaultedRadio(ui_defaults, "main_thundering", False,
                                   text="Thunder", group_id="weather")]
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
            return [[c1_layout, c2_layout]]

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
                    col2.add_row(
                        sg.CB("",
                              ui_defaults.get(key.lower(), gamerules.get(gr)),
                              key=key))
                else:
                    col2.add_row(
                        sg.I(ui_defaults.get(key.lower(), gamerules.get(gr)),
                             (10, 1), key=key))
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
                de.DefaultedCombo(ui_defaults, "terrain_generator", generators,
                                  "Default", size=(25, 1), pad=(3, 10),
                                  readonly=True, enable_events=True)
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
                de.DefaultedCombo(ui_defaults, "buffet_chunk_type",
                                  mu.buffet_chunk_gen, size=(25, 1),
                                  readonly=True, enable_events=True)
            ]]
            layout += [[
                sg.T("Default block", (15, 1)),
                de.DefaultedCombo(ui_defaults, "buffet_block",
                                  mu.get_mc_definitions("blocks"), "stone",
                                  size=(25, 1))
            ]]
            layout += [[
                sg.T("Default fluid", (15, 1)),
                de.DefaultedRadio(ui_defaults, "buffet_fluid_water", True,
                                  text="Water", group_id="buffet_fluid"),
                de.DefaultedRadio(ui_defaults, "buffet_fluid_lava", False,
                                  text="Lava", group_id="buffet_fluid")
            ]]
            layout += [[sg.Text("┈" * 46)]]
            layout += [[
                sg.T("Biomes distribution", (15, 1)),
                de.DefaultedCombo(ui_defaults, "buffet_biome_type",
                                  mu.buffet_types, size=(25, 1), readonly=True,
                                  enable_events=True)
            ]]
            layout += [[
                sg.T("Checkerboard size", (15, 1)),
                de.DefaultedSlider(ui_defaults, "buffet_size", 2,
                                   range=(-4, 16), orientation='h',
                                   tooltip="".join([
                                       "The biome squares will have sides of",
                                       "2^size chunks.\n -4 = 1 block\n",
                                       "16 = 65536 chunks"]))
            ]]
            layout += [[
                sg.T("Biomes", (15, 1)),
                sg.Col([
                    [de.DefaultedCB(ui_defaults, f"buffet_biomes_{b}", False,
                                    text=b)] for b in biomes], size=(175, 125),
                    pad=(5, 5), scrollable=True, vertical_scroll_only=True,
                    key="buffet_biomes")
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
                de.DefaultedCombo(ui_defaults, "flat_preset",
                                  list(superflat_dict.keys()),
                                  superflat_presets[0][0], size=(25, 1),
                                  readonly=True, enable_events=True)
            ]]
            layout += [[
                sg.T("Biome", (15, 1)),
                de.DefaultedCombo(ui_defaults, "flat_biome", biomes,
                                  superflat_presets[0][2], size=(25, 1),
                                  readonly=True)
            ]]
            layout += [[
                sg.T("Layers", (15, 1)),
                de.DefaultedInput(ui_defaults, "flat_layers",
                                  superflat_presets[0][1], size=(27, 1))
            ]]
            layout += [[
                sg.T("Structure flags", (15, 1)),
                de.DefaultedInput(ui_defaults, "flat_structures",
                                  superflat_presets[0][3], size=(27, 1))
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
                    sg.T("X"),
                    de.DefaultedInput(ui_defaults, "border_x", 0, size=(19, 1)),
                    sg.T("Z"),
                    de.DefaultedInput(ui_defaults, "border_z", 0, size=(19, 1)),
                ]])
            ]]
            col1_layout = [[
                sg.Frame("Border size", [
                    [
                        sg.T("Initial size", (8, 1)),
                        de.DefaultedInput(ui_defaults, "border_size",
                                          "60000000", size=(10, 1),
                                          justification="right")
                    ],
                    [
                        sg.T("Final size", (8, 1)),
                        de.DefaultedInput(ui_defaults, "border_size_target",
                                          "60000000", size=(10, 1),
                                          justification="right")
                    ],
                    [
                        sg.T("Lerp time", (8, 1),
                             tooltip="Seconds until border reaches final size"),
                        de.DefaultedInput(ui_defaults, "border_lerp_time", "0",
                                          size=(10, 1), justification="right")
                    ]
                ])
            ]]
            col2_layout = [[
                sg.T("Damage", (11, 1), tooltip="Damage per block"),
                de.DefaultedSpin(ui_defaults, "border_damage",
                                 [str(x / 10) for x in range(201)], "0.2",
                                 size=(7, 1))
            ]]
            col2_layout += [[
                sg.T("Safe distance", (11, 1), tooltip="Blocks beyond border"),
                de.DefaultedInput(ui_defaults, "border_safe_blocks", "5",
                                  size=(8, 1), justification="right")
            ]]
            col2_layout += [[
                sg.T("Warning time", (11, 1)),
                de.DefaultedInput(ui_defaults, "border_warn_time", "15",
                                  size=(8, 1), justification="right")
            ]]
            col2_layout += [[
                sg.T("Warning blocks", (11, 1)),
                de.DefaultedInput(ui_defaults, "border_warn_blocks", "5",
                                  size=(8, 1), justification="right")
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
                sg.ProgressBar(100, "horizontal", (20, 23), visible=False,
                               key="progress_bar")
            ]
        ]
        self.layout(main_layout)
        return self

    def Finalize(self):
        super(FwcWindow, self).Finalize()

        if self["terrain_generator"].get() != "Buffet":
            self["buffet_option_frame"].hide_row()
        if self["terrain_generator"].get() != "Flat":
            self["flat_option_frame"].hide_row()
        if self["buffet_biome_type"].get() != "Checkerboard":
            self["buffet_size"].hide_row()
        if self["main_all_versions"].get():
            self["main_release"].update(values=supported_versions,
                                        value=ui_defaults.get("main_release"))
        self["border_damage"].Widget.configure(justify="right")

    finalize = Finalize
