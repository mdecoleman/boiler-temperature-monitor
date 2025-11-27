from machine import Pin
import dht
import time
import json

DEFAULT_SENSOR_PIN = 15
DEFAULT_INTERVAL_SECONDS = 10


class Config:
    def __init__(self, data):
        self.monitoring_interval = data.get(
            "monitoring_interval", DEFAULT_INTERVAL_SECONDS
        )
        self.sensor_pin = data.get("sensor_pin", DEFAULT_SENSOR_PIN)
        self.api_key = data.get("api_key")
        self.api_url = data.get("api_url")


def load_config():
    try:
        with open("config.json") as f:
            data = json.load(f)
        return Config(data)
    except OSError:
        print("Warning: config.json not found, using defaults")
        return Config({})

def monitor():
    config = load_config()
    sensor = dht.DHT22(Pin(config.sensor_pin))

    while True:
        try:
            sensor.measure()
            temp = sensor.temperature()
            humidity = sensor.humidity()

            print(f"Temperature: {temp}\u00b0C, Humidity: {humidity}%")
        except OSError as e:
            print("Failed to read sensor:", e)
        time.sleep(config.monitoring_interval)


monitor()
