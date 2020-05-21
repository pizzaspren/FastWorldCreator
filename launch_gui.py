import PySimpleGUI as sg

from fast_world_creator import core
from fast_world_creator.utils.level_dat_utils import get_default_gamerules
from fast_world_creator.utils import common_utils as cu, minecraft_utils as mu, \
    datapack_utils

sg.theme('DarkAmber')  # Add a touch of color
sg.SetOptions(
    input_elements_background_color='#E9E9E9',
    input_text_color="#000000"
)

installed_versions = cu.find_installed_minecraft_versions()
available_datapacks = datapack_utils.get_available_datapacks()
available_datapacks.sort(key=lambda x: x.name)
difficulties = [d.name.title() for d in mu.Difficulties]
game_modes = [g.name.title() for g in mu.GameModes]
gamerules = get_default_gamerules()


def create_window_layout():
    tab1 = sg.Tab("Main", create_main_tab_layout())
    tab2 = sg.Tab("Gamerules", create_gamerule_layout())
    tab3 = sg.Tab("World gen", create_worldgen_layout())
    layout = [
        [sg.TabGroup([[tab1, tab2, tab3]])],
        [sg.Button('Ok'), sg.Button('Cancel')]
    ]
    return layout


def create_main_tab_layout():
    layout = [[
        sg.T('MC Version', size=(10, 1)),
        sg.Combo(
            [k for k in installed_versions.keys()],
            default_value=list(installed_versions.keys())[-1],
            size=(18, 1),
            readonly=True,
            key="release"
        )
    ]]
    layout += [[
        sg.T('World Name', size=(10, 1)),
        sg.I(size=(20, 1), key="name")
    ]]
    layout += [[
        sg.T('Seed', size=(10, 1), tooltip="Leave blank for random seed"),
        sg.I(
            size=(20, 1),
            tooltip="Leave blank for random seed",
            key="seed"
        )
    ]]
    layout += [[
        sg.T('Difficulty', size=(10, 1)),
        sg.Combo(
            difficulties,
            default_value=difficulties[0],
            size=(18, 1),
            readonly=True,
            key="difficulty"
        )
    ]]
    layout += [[
        sg.T('Game mode', size=(10, 1)),
        sg.Combo(
            game_modes,
            default_value=game_modes[0],
            size=(18, 1),
            readonly=True,
            key="game_mode"
        )
    ]]
    layout += [[sg.Frame(title='Datapacks', layout=create_datapack_layout())]]
    return layout


def create_datapack_layout():
    grouped_packs = [
        available_datapacks[i:i + 2] for i in
        range(0, len(available_datapacks), 2)
    ]
    c1_layout, c2_layout = [], []
    for d_pair in grouped_packs:
        c1_layout.append([
            sg.CB(
                default=True,
                text=d_pair[0].name,
                tooltip=d_pair[0].description,
                key=d_pair[0].name,
                size=(15, 1)
            )
        ])
        if len(d_pair) > 1:
            c2_layout.append([
                sg.CB(
                    default=True,
                    text=d_pair[1].name,
                    tooltip=d_pair[1].description,
                    key=d_pair[1].name,
                    size=(15, 1)
                )
            ])
    return [[sg.Column(c1_layout), sg.Column(c2_layout)]]


def create_gamerule_layout():
    grouped = sg.Column([[]], scrollable=True, vertical_scroll_only=True)
    for gr in gamerules.keys():
        col1, col2 = sg.Sizer(20, 1), sg.Sizer(15, 1)
        col2.ElementJustification = "right"
        col1.add_row(
            sg.CB(text="", visible=False),
            sg.Text(gr, size=(25, 1))
        )
        if isinstance(gamerules.get(gr), bool):
            col2.add_row(
                sg.CB(
                    default=gamerules.get(gr),
                    key=gr,
                    text="",
                )
            )
        else:
            col2.add_row(
                sg.I(
                    default_text=gamerules.get(gr),
                    key=gr,
                    size=(10, 1),
                    justification="right"
                )
            )
        grouped.add_row(col1, col2)

    return [[grouped]]


def create_worldgen_layout():
    weather_layout = []
    weather_layout += [
        sg.CB(text="Raining", key="rain"),
        sg.CB(text="Thundering", key="thunder"),
    ]
    layout = [[sg.Frame(title='Weather', layout=[weather_layout])]]
    return layout


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
        world_name=values.get("name"),
        seed=values.get("seed"),
        difficulty=difficulties.index(values.get("difficulty")),
        datapacks=[dp for dp in available_datapacks if values[dp.name]],
        gamerules=updated_gamerules,
        game_mode=game_modes.index(values.get("game_mode")),
        raining=values.get("rain"),
        thundering=values.get("thunder")
    )


# Create the Window
window = sg.Window(
    title='Fast world creator',
    layout=create_window_layout(),
    icon="assets/logo64.ico",)
while True:
    event, value_dict = window.read()
    if event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break
    if event == "Ok":
        create(value_dict)
        break

window.close()
