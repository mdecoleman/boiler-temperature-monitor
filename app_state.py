from screen_renderer import Screen


class AppState:
    def __init__(self):
        self.awake = True
        self.last_button_press = 0
        self.last_update = 0
        self.screen = Screen.HOME
