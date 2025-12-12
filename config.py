import json

DEFAULT_REFRESH_INTERVAL_SECONDS = 30
DEFAULT_SCREEN_TIMEOUT_SECONDS = 10


class Sensor:
    def __init__(self, id, label):
        self.id = id
        self.label = label


class Config:
    def __init__(
        self, refresh_interval: int, sensors: dict[str, Sensor], screen_timeout
    ):
        self.refresh_interval = refresh_interval
        self.sensors = sensors
        self.screen_timeout = screen_timeout


def validate_sensors(sensors):
    required_keys = ["temp_1", "temp_2", "temp_3"]

    for key in required_keys:
        if key not in sensors:
            raise ValueError(f"Missing sensor: {key}")

        sensor = sensors[key]

        if "id" not in sensor:
            raise ValueError(f"Sensor {key} missing 'id' field")

        if "label" not in sensor:
            raise ValueError(f"Sensor {key} missing 'label' field")

        if not sensor["id"].startswith("0x"):
            raise ValueError(f"Sensor {key} ID must start with '0x': {sensor['id']}")


def validate_refresh_interval(config):
    refresh_interval = config["refresh_interval"]

    if not isinstance(refresh_interval, int):
        raise ValueError("refresh_interval must be an integer")

    if refresh_interval < 0:
        raise ValueError("refresh_interval must be >= 0")


def load_config(config_path="config.json"):
    try:
        with open(config_path, "r") as f:
            config = json.load(f)

        if "sensors" not in config:
            raise ValueError("Config must contain 'sensors' section")

        validate_sensors(config["sensors"])

        if "refresh_interval" not in config:
            config["refresh_interval"] = DEFAULT_REFRESH_INTERVAL_SECONDS
        else:
            validate_refresh_interval(config)

        sensor_objects = {
            key: Sensor(s["id"], s["label"]) for key, s in config["sensors"].items()
        }

        return Config(
            refresh_interval=config["refresh_interval"],
            sensors=sensor_objects,
            screen_timeout=DEFAULT_SCREEN_TIMEOUT_SECONDS,
        )

    except OSError as e:
        raise OSError(f"Config file not found: {config_path}") from e
    except (ValueError, KeyError) as e:
        raise ValueError(f"Invalid config: {e}") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}") from e
