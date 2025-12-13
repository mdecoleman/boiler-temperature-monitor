import network
import utime
import bluetooth
import machine


class Pico2W:
    def disable_ble(self):
        try:
            utime.sleep(0.5)

            try:
                bluetooth.BLE().active(False)
                print("Bluetooth disabled")
            except (ImportError, AttributeError, Exception):
                pass

        except Exception as e:
            print(f"Error disabling BLE: {e}")

        return self

    def disable_wifi(self):
        try:
            utime.sleep(0.5)

            try:
                wlan = network.WLAN(network.STA_IF)
                wlan.active(False)
                print("WiFi disabled")
            except Exception:
                pass

        except Exception as e:
            print(f"Error disabling WiFi: {e}")

        return self

    def sleep(self):
        machine.freq(24000000)

        print("CPU downclocked to 24MHz")

        return self

    def wake(self):
        machine.freq(150000000)

        print("CPU clock restored to 150MHz")

        return self
