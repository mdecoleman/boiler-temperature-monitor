PADDING = 8
LINE_HEIGHT = 8


class Screen:
    HOME = 0
    SENSOR_1 = 1
    SENSOR_2 = 2
    SENSOR_3 = 3


def _find_sensor_by_id(sensors, id):
    for s in sensors:
        if s["id"] == id:
            return s

    return None


def _get_line_position(line):
    line_position = PADDING

    if line > 1:
        previous_lines = line - 1
        line_position += (PADDING + LINE_HEIGHT) * previous_lines
    elif line < 1:
        raise ValueError("Line number must be greater than or equal to 1")

    return line_position


def _render_sensor_reading(lcd, sensors, sensor_key, start_line, config):
    sensor = config.sensors.get(sensor_key)

    if sensor == None:
        raise ValueError(f"Sensor with key: {sensor_key} not found")

    sensor_id = sensor.id
    label = sensor.label

    sensor_reading = _find_sensor_by_id(sensors, sensor_id)

    if sensor_reading == None:
        raise ValueError(
            f"Could not find readings for sensor id:{sensor_id}, label:{label}"
        )

    temp = sensor_reading["temp"]

    lcd.text(label, PADDING, _get_line_position(start_line), lcd.WHITE)
    lcd.text(f"{temp:.1f} C", PADDING, _get_line_position(start_line + 1), lcd.WHITE)


def render_home_screen(lcd, sensors, config):
    _render_sensor_reading(lcd, sensors, "temp_1", 1, config)

    lcd.line(
        0,
        _get_line_position(3) + (LINE_HEIGHT // 2),
        320,
        _get_line_position(3) + (LINE_HEIGHT // 2),
        lcd.DARK_GRAY,
    )

    _render_sensor_reading(lcd, sensors, "temp_2", 4, config)

    lcd.line(
        0,
        _get_line_position(6) + (LINE_HEIGHT // 2),
        320,
        _get_line_position(6) + (LINE_HEIGHT // 2),
        lcd.DARK_GRAY,
    )

    _render_sensor_reading(lcd, sensors, "temp_3", 7, config)


def render_sensor_screen(lcd, sensors, sensor_key, config):
    _render_sensor_reading(lcd, sensors, sensor_key, 1, config)


def render_error_message(lcd, err):
    lcd.fill(lcd.BLACK)

    error_text = str(err)

    max_chars = 40
    words = error_text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + (" " if current_line else "") + word

        if len(test_line) <= max_chars:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    if len(lines) > 12:
        lines = lines[:12]
        lines[-1] = lines[-1][:37] + "..."

    y_position = PADDING
    lcd.text("Error:", PADDING, y_position, lcd.RED)
    y_position += LINE_HEIGHT + PADDING

    for line in lines:
        lcd.text(line, PADDING, y_position, lcd.WHITE)
        y_position += LINE_HEIGHT + PADDING

    lcd.show()


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
