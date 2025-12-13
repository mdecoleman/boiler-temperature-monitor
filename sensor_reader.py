from constants import SENSOR_PIN
from machine import Pin
import ds18x20
import onewire
import utime


class SensorReader:
    def __init__(self):
        self._pin = Pin(SENSOR_PIN, Pin.IN)
        self._one_wire_bus = onewire.OneWire(self._pin)
        self._one_wire_sensors = ds18x20.DS18X20(self._one_wire_bus)
        self._sensor_ids = None

    def _set_9bit_precision(self):
        if self._sensor_ids is None:
            raise RuntimeError("Cannot set precision before sensors are scanned")

        for sensor_id in self._sensor_ids:
            self._one_wire_bus.reset()
            self._one_wire_bus.select_rom(sensor_id)
            self._one_wire_bus.writebyte(0x4E)
            self._one_wire_bus.writebyte(0x00)
            self._one_wire_bus.writebyte(0x00)
            self._one_wire_bus.writebyte(0x1F)
            self._one_wire_bus.reset()

    def read_all(self):
        sensors = []

        try:
            if self._sensor_ids is None:
                self._sensor_ids = self._one_wire_sensors.scan()
                self._set_9bit_precision()

            count = len(self._sensor_ids)

            if count == 0:
                raise OSError("No sensors found on OneWire bus")

            if count < 3:
                raise OSError(f"Expected 3 temperature sensors, {count} found")

            self._one_wire_sensors.convert_temp()
            utime.sleep(0.1)

            for id in self._sensor_ids:
                rom_hex = hex(int.from_bytes(id, "little"))
                temp = self._one_wire_sensors.read_temp(id)
                sensors.append({"id": rom_hex, "temp": temp})

        except Exception as e:
            print(f"Error scanning sensors: {e}")

        return sensors
