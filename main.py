from buttons import init_buttons
from config import  load_config
from lcd import LCD
from renderer import ( render_home_screen, render_sensor_screen, render_error_message )
from sensor_monitor import SensorsMonitor
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
}


def monitor():
    lcd = LCD()

    gc.collect()

    try:
        init_buttons(app_state)

        sensors_monitor = SensorsMonitor()

        last_read = 0
        read_interval = config.refresh_interval * 1000

        first_render = True
        last_screen = app_state["screen"]

        sensors = []

        while True:
            gc.collect()

            current_screen = app_state["screen"]
            screen_changed = last_screen != current_screen

            current_time = utime.ticks_ms()
            should_read = (utime.ticks_diff(current_time, last_read)) > read_interval

            if should_read:
                print(f"Reading sensors")
                sensors = sensors_monitor.read_sensors()
                last_read = current_time

            if screen_changed or first_render or should_read:
                lcd.fill(lcd.BLACK)

                if app_state["screen"] == Screen.HOME:
                    render_home_screen(lcd, sensors)
                elif app_state["screen"] == Screen.SENSOR_1:
                    render_sensor_screen(lcd, sensors,  "temp_1")
                elif app_state["screen"] == Screen.SENSOR_2:
                    render_sensor_screen(lcd, sensors,  "temp_2")
                elif app_state["screen"] == Screen.SENSOR_3:
                    render_sensor_screen(lcd, sensors, "temp_3")
                else:
                    raise ValueError(
                        f"Unable to render screen {app_state['screen']}: No renderer available"
                    )

                print(f"Screen render: {current_screen}")

                lcd.show()

            first_render = False
            last_screen = current_screen

            utime.sleep(0.05)
    except Exception as e:
        print(f"Could not render data: {e}")
        render_error_message(lcd, e)


if __name__ == "__main__":
    monitor()