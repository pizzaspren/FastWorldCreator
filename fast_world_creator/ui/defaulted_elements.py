import PySimpleGUI as sg


class DefaultedInput(sg.I):
    def __init__(self, ui_defaults, key, default="", *args, **kwargs):
        super().__init__(
            default_text=ui_defaults.get(key, default), key=key,
            *args, **kwargs)


class DefaultedCombo(sg.Combo):
    def __init__(self, ui_defaults, key, values, default="", *args, **kwargs):
        values = values or []
        super().__init__(
            values,
            default_value=ui_defaults.get(key, default) or values[0], key=key,
            *args, **kwargs)


class DefaultedSlider(sg.Slider):
    def __init__(self, ui_defaults, key, default="", *args, **kwargs):
        super().__init__(
            default_value=ui_defaults.get(key, default), key=key,
            *args, **kwargs)


class DefaultedRadio(sg.Radio):
    def __init__(self, ui_defaults, key, default="", *args, **kwargs):
        super().__init__(
            default=ui_defaults.get(key, default), key=key,
            *args, **kwargs)


class DefaultedCB(sg.CB):
    def __init__(self, ui_defaults, key, default="", *args, **kwargs):
        super().__init__(
            default=ui_defaults.get(key, default), key=key,
            *args, **kwargs)


class DefaultedSpin(sg.Spin):
    def __init__(self, ui_defaults, key, values, default="", *args, **kwargs):
        super().__init__(
            values,
            initial_value=ui_defaults.get(key, default), key=key,
            *args, **kwargs)
