from buttons import init_buttons
from config import load_config
from lcd import LCD
from renderer import render_home_screen, render_sensor_screen, render_error_message
from sensor_monitor import SensorsMonitor

import gc
import utime
import wirless

try:
    config = load_config()
except OSError:
    print("ERROR: config.json not found!")
    raise OSError("config.json file is required")
except ValueError as e:
    print(f"ERROR: Invalid config.json: {e}")
    raise


class Screen:
    HOME = 0
    SENSOR_1 = 1
    SENSOR_2 = 2
    SENSOR_3 = 3


app_state = {
    "awake": True,
    "last_button_press": 0,
    "last_update": 0,
    "screen": Screen.HOME,
}

renderers = {
    Screen.HOME: lambda lcd, sensors, cfg: render_home_screen(lcd, sensors, cfg),
    Screen.SENSOR_1: lambda lcd, sensors, cfg: render_sensor_screen(
        lcd, sensors, "temp_1", cfg
    ),
    Screen.SENSOR_2: lambda lcd, sensors, cfg: render_sensor_screen(
        lcd, sensors, "temp_2", cfg
    ),
    Screen.SENSOR_3: lambda lcd, sensors, cfg: render_sensor_screen(
        lcd, sensors, "temp_3", cfg
    ),
}


def monitor():
    wirless.disable()

    lcd = LCD()
    lcd.wake()

    gc.collect()

    try:
        init_buttons(app_state)

        sensors_monitor = SensorsMonitor()

        refresh_interval = config.refresh_interval * 1000
        screen_timeout = config.screen_timeout * 1000

        screen = app_state["screen"]

        sensors = sensors_monitor.read_sensors()

        while True:
            current_time = utime.ticks_ms()

            awake = app_state["awake"]
            current_screen = app_state["screen"]
            last_button_press = app_state["last_button_press"]
            last_update = app_state["last_update"]

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
                    app_state["awake"] = False
                    print("Asleep")
            elif not awake:
                lcd.wake()
                renderers[app_state["screen"]](lcd, sensors, config)
                lcd.show()
                app_state["awake"] = True
                print("Awake")
            elif screen_changed:
                screen = current_screen
                lcd.clear()
                renderers[app_state["screen"]](lcd, sensors, config)
                lcd.show()

                print(f"Screen changed to {current_screen}")
            elif should_update:
                sensors = sensors_monitor.read_sensors()
                gc.collect()

                app_state["last_update"] = current_time

                renderers[app_state["screen"]](lcd, sensors, config)
                lcd.show()

                print(f"Refreshed data")

            utime.sleep(0.05)
    except Exception as e:
        print(f"Could not render data: {e}")
        render_error_message(lcd, e)


if __name__ == "__main__":
    monitor()
