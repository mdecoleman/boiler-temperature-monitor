from buttons import init_buttons
from config import load_config
from lcd import LCD
from renderer import render_home_screen, render_sensor_screen, render_error_message
from sensor_monitor import SensorsMonitor
import wirless
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


class Screen:
    HOME = 0
    SENSOR_1 = 1
    SENSOR_2 = 2
    SENSOR_3 = 3


app_state = {
    "screen": Screen.HOME,
    "last_button_press": utime.ticks_ms(),
    "awake": True,
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
    gc.collect()

    try:
        init_buttons(app_state)

        sensors_monitor = SensorsMonitor()

        last_read = 0
        read_interval = config.refresh_interval * 1000
        screen_timeout = config.screen_timeout * 1000

        last_screen = app_state["screen"]

        print(f"Reading sensors")
        sensors = sensors_monitor.read_sensors()

        while True:
            current_time = utime.ticks_ms()
            current_screen = app_state["screen"]
            screen_changed = last_screen != current_screen

            should_turn_off_screen = (
                utime.ticks_diff(current_time, app_state["last_button_press"])
                > screen_timeout
            )

            if should_turn_off_screen:
                if app_state["awake"]:
                    print("Turning off screen")
                    lcd.sleep()
                    app_state["awake"] = False
            else:
                should_read = (
                    utime.ticks_diff(current_time, last_read)
                ) > read_interval

                if should_read:
                    print(f"Reading sensors")
                    sensors = sensors_monitor.read_sensors()
                    last_read = current_time
                    gc.collect()

                should_render = screen_changed or should_read

                if should_render:
                    print("rendering screen")
                    lcd.wake()
                    app_state["awake"] = True

                    if app_state["screen"] not in renderers:
                        raise ValueError(
                            f"Unable to render screen {app_state['screen']}: No renderer available"
                        )

                    renderers[app_state["screen"]](lcd, sensors, config)
                    print(f"Screen render: {current_screen}")
                    lcd.show()
                    gc.collect()

            last_screen = current_screen

            utime.sleep(0.05)
    except Exception as e:
        print(f"Could not render data: {e}")
        render_error_message(lcd, e)


if __name__ == "__main__":
    monitor()
