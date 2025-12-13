import asyncio
from app_state import AppState
from config import Config
from lcd import LCD
from pico import Pico2W
from screen_renderer import render_error_message, renderers
from sensor_reader import SensorReader

import button_handler
import gc
import utime


class Monitor:
    def __init__(self, config: Config):
        self._initialized = False

        self._config = config
        self._pico2W = Pico2W()
        self._screen = LCD()
        self._sensor_reader = SensorReader()
        self._app_state = AppState()

        self._sensors = []
        self._screen_timeout_ms = config.screen_timeout * 1000
        self._refresh_interval_ms = config.refresh_interval * 1000

    def _throw_if_not_initalized(self):
        if self._initialized:
            return

        raise OSError(
            "Monitor class is not initalized. Please call 'initialize()' before using this class."
        )

    def _sleep(self):
        self._throw_if_not_initalized()

        print("Sleeping")

        self._pico2W.sleep()
        self._screen.sleep()
        self._app_state.awake = False

    def _wake(self):
        self._throw_if_not_initalized()

        print("Waking")

        self._pico2W.wake()
        self._screen.wake()
        self._app_state.awake = True

    def _should_sleep(self):
        return (
            utime.ticks_diff(utime.ticks_ms(), self._app_state.last_button_press)
            > self._screen_timeout_ms
        )

    def _should_wake(self):
        return not self._should_sleep and not self._app_state.awake

    def _should_read(self):
        return (
            utime.ticks_diff(utime.ticks_ms(), self._app_state.last_read)
        ) > self._refresh_interval_ms

    async def initialize(self):
        print("Initializing")
        print("--------------------")
        await self._pico2W.disable_ble()
        await self._pico2W.disable_wifi()

        button_handler.init(self._app_state)

        self._sensors = await self._sensor_reader.read_all()

        self._initialized = True
        print("--------------------")

    async def run(self):
        self._throw_if_not_initalized()

        previous_screen = self._app_state.screen

        while True:
            current_screen = self._app_state.screen
            screen_changed = previous_screen != current_screen

            if self._should_sleep():
                if self._app_state.awake:
                    self._sleep()
            elif self._should_wake():
                self._wake()

                renderers[self._app_state.screen](
                    self._screen, self._sensors, self._config
                )
                self._screen.show()
            elif screen_changed:
                previous_screen = current_screen

                self._screen.clear()
                renderers[self._app_state.screen](
                    self._screen, self._sensors, self._config
                )
                self._screen.show()
            elif self._should_read():
                self._sensors = await self._sensor_reader.read_all()
                gc.collect()

                self._app_state.last_read = utime.ticks_ms()

                renderers[self._app_state.screen](
                    self._screen, self._sensors, self._config
                )

            if self._app_state.awake:
                await asyncio.sleep_ms(50)
            else:
                await asyncio.sleep_ms(500)
