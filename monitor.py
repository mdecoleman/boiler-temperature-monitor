from app_state import AppState
from lcd import LCD
from pico import Pico2W
from sensor_reader import SensorReader


class Monitor:
    def __init__(self):
        self._pico2W = Pico2W()
        self._screen = LCD()
        self._sensor_reader = SensorReader()
        self._state = AppState()

    def _sleep(self):
        print("Sleeping")

        self._pico2W.sleep()
        self._screen.sleep()
        self._state.awake = False

    def _wake(self):
        print("Waking")

        self._pico2W.wake()
        self._screen.wake()
        self._state.awake = True
