import network
import utime
import bluetooth
import machine
import asyncio


class Pico2W:
    async def disable_ble(self):
        """Asynchronously disable Bluetooth"""
        try:
            # Small delay to ensure BLE is ready to be disabled
            await asyncio.sleep_ms(100)

            try:
                ble = bluetooth.BLE()
                ble.active(False)
                print("Bluetooth disabled")
            except (ImportError, AttributeError) as e:
                print(f"BLE not available: {e}")
            except Exception as e:
                print(f"Error disabling BLE: {e}")

        except Exception as e:
            print(f"Unexpected error disabling BLE: {e}")

    async def disable_wifi(self):
        """Asynchronously disable WiFi"""
        try:
            # Small delay to ensure WiFi is ready to be disabled
            await asyncio.sleep_ms(100)

            try:
                wlan = network.WLAN(network.STA_IF)
                wlan.active(False)
                print("WiFi disabled")
            except Exception as e:
                print(f"Error disabling WiFi: {e}")

        except Exception as e:
            print(f"Unexpected error disabling WiFi: {e}")

    def sleep(self):
        machine.freq(24000000)

        print("CPU downclocked to 24MHz")

    def wake(self):
        machine.freq(150000000)

        print("CPU clock restored to 150MHz")
