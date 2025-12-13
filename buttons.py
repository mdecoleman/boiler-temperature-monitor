from constants import (
    BUTTON_PIN_BOTTOM_LEFT,
    BUTTON_PIN_BOTTOM_RIGHT,
    BUTTON_PIN_TOP_LEFT,
    BUTTON_PIN_TOP_RIGHT,
)
from machine import Pin
import asyncio
import utime


class ButtonType:
    BOTTOM_RIGHT = BUTTON_PIN_BOTTOM_RIGHT
    BOTTOM_LEFT = BUTTON_PIN_BOTTOM_LEFT
    TOP_RIGHT = BUTTON_PIN_TOP_RIGHT
    TOP_LEFT = BUTTON_PIN_TOP_LEFT


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
        """IRQ handler that schedules async callback"""
        current_time = utime.ticks_ms()
        current_state = self.pin.value()

        if current_state != self.last_state:
            if (
                utime.ticks_diff(current_time, self.last_trigger_time)
                > self.debounce_ms
            ):
                self.last_state = current_state
                self.last_trigger_time = current_time

                if current_state == 0:
                    asyncio.create_task(self.callback(self.button_id))


def create_async_button_handler(app_state):
    async def on_button_press_async(button_id):
        was_awake = app_state.awake
        app_state.last_button_press = utime.ticks_ms()

        await asyncio.sleep_ms(10)

        if not was_awake:
            return

        if button_id == ButtonType.TOP_LEFT:
            app_state.screen = (app_state.screen + 1) % 4

        elif button_id == ButtonType.TOP_RIGHT:
            pass

        elif button_id == ButtonType.BOTTOM_LEFT:
            pass

        elif button_id == ButtonType.BOTTOM_RIGHT:
            pass

    return on_button_press_async


def init_buttons(app_state):
    handler = create_async_button_handler(app_state)

    Button(ButtonType.TOP_LEFT, callback=handler)
    Button(ButtonType.TOP_RIGHT, callback=handler)
    Button(ButtonType.BOTTOM_LEFT, callback=handler)
    Button(ButtonType.BOTTOM_RIGHT, callback=handler)
