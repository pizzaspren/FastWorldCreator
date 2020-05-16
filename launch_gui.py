import PySimpleGUIQt as sg

from fast_world_creator import core
from fast_world_creator.utils import common_utils as cu, minecraft_utils as mu, \
    datapack_utils

sg.theme('DarkAmber')  # Add a touch of color

installed_versions = cu.find_installed_minecraft_versions()
available_datapacks = datapack_utils.get_available_datapacks()
available_datapacks.sort(key=lambda x: x.name)
difficulties = [d.name.title() for d in mu.Difficulties]


def create_layout():
    layout = [[
        sg.T('MC Version', size=(10, 1)),
        sg.Stretch(),
        sg.Combo(
            [k for k in installed_versions.keys()],
            size=(19.5, 1),
            readonly=True)]]
    layout += [[
        sg.T('World Name', size=(10, 1)),
        sg.Stretch(),
        sg.I(size=(20, 1))]]
    layout += [[
        sg.T('Seed', size=(10, 1), tooltip="Leave blank for random seed"),
        sg.Stretch(),
        sg.I(size=(20, 1), tooltip="Leave blank for random seed")]]
    layout += [[
        sg.T('Difficulty', size=(10, 1)),
        sg.Stretch(),
        sg.Combo(
            difficulties,
            size=(19.5, 1),
            readonly=True)]]
    layout += [[sg.Frame(title='Datapacks', layout=create_datapack_layout())]]
    layout += [[sg.Button('Ok'), sg.Button('Cancel')]]
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
                key=d_pair[0].name
            ),
            sg.Stretch()
        ])
        c2_layout.append([
            sg.CB(
                default=True,
                text=d_pair[1].name,
                tooltip=d_pair[1].description,
                key=d_pair[1].name
            ),
            sg.Stretch()
        ])
    return [[sg.Column(c1_layout), sg.Column(c2_layout)]]


def create(values: dict) -> None:
    sent_values = list(values.values())
    core.run(
        version_pair=(sent_values[0], installed_versions[sent_values[0]]),
        world_name=sent_values[1],
        seed=sent_values[2],
        difficulty=difficulties.index(sent_values[3]),
        datapacks=[dp for dp in available_datapacks if values[dp.name]]
    )


# Create the Window
window = sg.Window(
    title='Fast world creator',
    layout=create_layout())
while True:
    event, value_dict = window.read()
    if event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break
    if event == "Ok":
        create(value_dict)
        break

window.close()
