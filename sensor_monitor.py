from machine import Pin
import onewire
import utime
import ds18x20

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