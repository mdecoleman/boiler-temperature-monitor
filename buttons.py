from machine import Pin
import utime


class ButtonType:
    BOTTOM_RIGHT = 2
    BOTTOM_LEFT = 3
    TOP_RIGHT = 14
    TOP_LEFT = 15


class Button:
    def __init__(self, pin, callback):
        self.button_id = pin
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.callback = callback

        self.last_trigger_time = 0
        self.debounce_ms = 200
        self.last_state = 1

        self.pin.irq(
            trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self._irq_handler
        )

    def _irq_handler(self, _):
        current_time = utime.ticks_ms()
        current_state = self.pin.value()

        if utime.ticks_diff(current_time, self.last_trigger_time) > self.debounce_ms:
            if self.last_state == 1 and current_state == 0:
                self.last_trigger_time = current_time
                self.last_state = current_state
                self.callback(self.button_id)
            elif self.last_state == 0 and current_state == 1:
                self.last_trigger_time = current_time
                self.last_state = current_state


def on_button_press(button_id):
    state["last_button_press"] = utime.ticks_ms()

    if state["awake"] == False:
        return

    if button_id == ButtonType.TOP_LEFT:
        state["screen"] = (state["screen"] + 1) % 4

    elif button_id == ButtonType.TOP_RIGHT:
        pass

    elif button_id == ButtonType.BOTTOM_LEFT:
        pass

    elif button_id == ButtonType.BOTTOM_RIGHT:
        pass


def init_buttons(app_state):
    global state
    state = app_state

    Button(ButtonType.TOP_LEFT, callback=on_button_press)
    Button(ButtonType.TOP_RIGHT, callback=on_button_press)
    Button(ButtonType.BOTTOM_LEFT, callback=on_button_press)
    Button(ButtonType.BOTTOM_RIGHT, callback=on_button_press)
