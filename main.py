from machine import Pin
import gc
import onewire
import ds18x20
import utime
from lcd import LCD
from buttons import init_buttons

PADDING = 8
DEFAULT_INTERVAL_SECONDS = 5
LINE_HEIGHT = 8


SENSORS_MAP = {
    "temp_1": {"id": "0xb20b2551d0e81428", "name": "Temp 1"},
    "temp_2": {"id": "0xb10b2551cf9fc728", "name": "Temp 2"},
    "temp_3": {"id": "0x460b2551a7326c28", "name": "Temp 3"},
}


class Screen:
    HOME = 0
    SENSOR_1 = 1
    SENSOR_2 = 2
    SENSOR_3 = 3


app_state = {
    "screen": Screen.HOME,
}


class SensorsMonitor:
    def __init__(self):
        self._pin = Pin(18, Pin.IN)
        self._one_wire_bus = onewire.OneWire(self._pin)
        self._one_wire_sensors = ds18x20.DS18X20(self._one_wire_bus)

    def read_sensors(self):
        sensors = []

        try:
            sensor_ids = self._one_wire_sensors.scan()
            count = len(sensor_ids)

            if count == 0:
                raise OSError("No sensors found on OneWire bus")

            if count < 3:
                raise OSError(f"Expected 3 temperature sensors, {count} found")

            self._one_wire_sensors.convert_temp()
            utime.sleep(0.75)

            for id in sensor_ids:
                rom_code = hex(int.from_bytes(id, "little"))
                temperature = self._one_wire_sensors.read_temp(id)
                sensors.append({"id": rom_code, "temp": temperature})

        except Exception as e:
            print(f"Error scanning sensors: {e}")

        return sensors


def find_sensor_by_id(sensors, id):
    for s in sensors:
        if s["id"] == id:
            return s

    return None


def get_color_for_temp(lcd, temp):
    """Return color based on temperature thresholds"""
    if temp > 70:
        return lcd.RED
    elif temp > 65:
        return lcd.YELLOW
    elif temp < 55:
        return lcd.BLUE
    else:
        return lcd.WHITE


def get_line_position(line):
    line_position = PADDING

    if line > 1:
        previous_lines = line - 1
        line_position += (PADDING + LINE_HEIGHT) * previous_lines
    elif line < 1:
        raise ValueError("Line number must be greater than or equal to 1")

    return line_position


def render_sensor_reading(lcd, sensors, key, start_line):
    sensor = SENSORS_MAP.get(key)

    if sensor == None:
        raise ValueError(f"Sensor with key: {key} not found")

    sensor_id = sensor["id"]
    label = sensor["name"]

    sensor_reading = find_sensor_by_id(sensors, sensor_id)

    if sensor_reading == None:
        raise ValueError(f"Could not find readings for sensor key: {key}")

    temp = sensor_reading["temp"]

    lcd.text(label, PADDING, get_line_position(start_line), lcd.WHITE)
    lcd.text(f"{temp:.1f} C", PADDING, get_line_position(start_line + 1), lcd.WHITE)


def render_home_screen(lcd, sensors):
    render_sensor_reading(lcd, sensors, "temp_1", 1)

    lcd.line(
        0,
        get_line_position(3) + (LINE_HEIGHT // 2),
        320,
        get_line_position(3) + (LINE_HEIGHT // 2),
        lcd.DARK_GRAY,
    )

    render_sensor_reading(lcd, sensors, "temp_2", 4)

    lcd.line(
        0,
        get_line_position(6) + (LINE_HEIGHT // 2),
        320,
        get_line_position(6) + (LINE_HEIGHT // 2),
        lcd.DARK_GRAY,
    )

    render_sensor_reading(lcd, sensors, "temp_3", 7)


def render_sensor_screen(lcd, sensors, key):
    render_sensor_reading(lcd, sensors, key, 1)


def render_current_screen(lcd, sensors, screen):
    """Render the current screen based on screen value"""
    lcd.fill(lcd.BLACK)

    if screen == Screen.HOME:
        render_home_screen(lcd, sensors)
    elif screen == Screen.SENSOR_1:
        render_sensor_screen(lcd, sensors, "temp_1")
    elif screen == Screen.SENSOR_2:
        render_sensor_screen(lcd, sensors, "temp_2")
    elif screen == Screen.SENSOR_3:
        render_sensor_screen(lcd, sensors, "temp_3")

    lcd.show()


def monitor():
    lcd = LCD()

    gc.collect()

    init_buttons(app_state)

    sensors_monitor = SensorsMonitor()

    last_read = 0
    read_interval = DEFAULT_INTERVAL_SECONDS * 1000

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
                lcd.text("Sensor 1", 0, 0, lcd.WHITE)
            elif app_state["screen"] == Screen.SENSOR_2:
                lcd.text("Sensor 2", 0, 0, lcd.WHITE)
            elif app_state["screen"] == Screen.SENSOR_3:
                lcd.text("Sensor 3", 0, 0, lcd.WHITE)
            else:
                raise ValueError(
                    f"Unable to render screen {app_state['screen']}: Not renderer available"
                )

            print(f"Screen render: {current_screen}")

            lcd.show()

        first_render = False
        last_screen = current_screen

        utime.sleep(0.05)


if __name__ == "__main__":
    monitor()
