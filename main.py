from app_state import AppState
from buttons import init_buttons
from config import load_config
from lcd import LCD
from pico import Pico2W
from screen_renderer import (
    render_error_message,
    renderers,
)
from sensor_reader import SensorReader

import asyncio
import gc
import utime

try:
    config = load_config()
except OSError:
    print("ERROR: config.json not found!")
    raise OSError("config.json file is required")
except ValueError as e:
    print(f"ERROR: Invalid config.json: {e}")
    raise


app_state = AppState()


async def monitor():
    pico2W = Pico2W()

    await pico2W.disable_wifi()
    await pico2W.disable_ble()

    lcd = LCD()
    lcd.wake()

    gc.collect()

    try:
        init_buttons(app_state)

        sensor_reader = SensorReader()

        refresh_interval = config.refresh_interval * 1000
        screen_timeout = config.screen_timeout * 1000

        screen = app_state.screen

        sensors = sensor_reader.read_all()

        while True:
            current_time = utime.ticks_ms()

            awake = app_state.awake
            current_screen = app_state.screen
            last_button_press = app_state.last_button_press
            last_update = app_state.last_update

            screen_changed = screen != current_screen

            should_sleep = (
                utime.ticks_diff(current_time, last_button_press) > screen_timeout
            )

            should_update = (
                utime.ticks_diff(current_time, last_update)
            ) > refresh_interval

            if should_sleep:
                if awake:
                    lcd.sleep()
                    pico2W.sleep()
                    app_state.awake = False
                    print("Asleep")
            elif not awake:
                pico2W.wake()
                lcd.wake()
                renderers[app_state.screen](lcd, sensors, config)
                lcd.show()
                app_state.awake = True
                print("Awake")
            elif screen_changed:
                screen = current_screen
                lcd.clear()
                renderers[app_state.screen](lcd, sensors, config)
                lcd.show()

                print(f"Screen changed to {current_screen}")
            elif should_update:
                sensors = sensor_reader.read_all()
                gc.collect()

                app_state.last_update = current_time

                renderers[app_state.screen](lcd, sensors, config)
                lcd.show()

                print(f"Refreshed data")

            if awake:
                utime.sleep(0.05)
            else:
                utime.sleep(0.5)
    except Exception as e:
        print(f"Could not render data: {e}")
        render_error_message(lcd, e)


if __name__ == "__main__":
    asyncio.run(monitor())
