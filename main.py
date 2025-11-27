from machine import Pin
import dht
import time

SENSOR_PIN = 15
INTERVAL_SECONDS = 2


def get_sensor():
    return dht.DHT22(Pin(SENSOR_PIN))


def read_sensor():
    sensor = get_sensor()
    sensor.measure()
    
    temp = sensor.temperature()
    humidity = sensor.humidity()
    
    return temp, humidity



def monitor():
    while True:
        try:
            temp, humidity = read_sensor()
            print(f"Temperature: {temp}\u00b0C, Humidity: {humidity}%")
        except OSError as e:
            print("Failed to read sensor:", e)
        time.sleep(INTERVAL_SECONDS)

monitor()