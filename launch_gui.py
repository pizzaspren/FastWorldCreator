import PySimpleGUI as sg

from fast_world_creator import core
from fast_world_creator.new_world.level_dat import get_default_gamerules
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
gamerules = get_default_gamerules()


def create_window_layout():
    tab1 = sg.Tab("Main", create_main_tab_layout())
    tab2 = sg.Tab("Gamerules", create_gamerule_layout())
    layout = [
        [
            sg.TabGroup([[tab1, tab2]])
        ],
        [
            sg.Button('Ok'), sg.Button('Cancel')
        ]
    ]
    return layout


def create_main_tab_layout():
    layout = [[
        sg.T('MC Version', size=(10, 1)),
        sg.Combo(
            [k for k in installed_versions.keys()],
            default_value=list(installed_versions.keys())[-1],
            size=(18, 1),
            readonly=True
        )
    ]]
    layout += [[
        sg.T('World Name', size=(10, 1)),
        sg.I(size=(20, 1))
    ]]
    layout += [[
        sg.T('Seed', size=(10, 1), tooltip="Leave blank for random seed"),
        sg.I(
            size=(20, 1),
            tooltip="Leave blank for random seed",
        )
    ]]
    layout += [[
        sg.T('Difficulty', size=(10, 1)),
        sg.Combo(
            difficulties,
            default_value=difficulties[0],
            size=(18, 1),
            readonly=True,
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
            ),
            sg.Stretch()
        ])
        c2_layout.append([
            sg.CB(
                default=True,
                text=d_pair[1].name,
                tooltip=d_pair[1].description,
                key=d_pair[1].name,
                size=(15, 1)
            ),
            sg.Stretch()
        ])
    return [[sg.Column(c1_layout), sg.Column(c2_layout)]]


def create_gamerule_layout():
    grouped = sg.Column([[]], scrollable=True, vertical_scroll_only=True,)
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


def create(values: dict) -> None:
    sent_values = list(values.values())
    updated_gamerules = dict()
    for gr in gamerules:
        updated_gamerules[gr] = str(values.get(gr)).lower()
    core.run(
        version_pair=(sent_values[0], installed_versions[sent_values[0]]),
        world_name=sent_values[1],
        seed=sent_values[2],
        difficulty=difficulties.index(sent_values[3]),
        datapacks=[dp for dp in available_datapacks if values[dp.name]],
        gamerules=updated_gamerules
    )


# Create the Window
window = sg.Window(
    title='Fast world creator',
    layout=create_window_layout())
while True:
    event, value_dict = window.read()
    if event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break
    if event == "Ok":
        create(value_dict)
        break

window.close()
