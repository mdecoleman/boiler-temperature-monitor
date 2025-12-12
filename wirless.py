import network
import utime


def disable():
    try:
        # Give the wireless chip time to initialize before attempting to disable
        utime.sleep(0.5)

        try:
            wlan = network.WLAN(network.STA_IF)
            wlan.active(False)
            print("WiFi disabled")
        except Exception:
            # Chip may not be available or already initialized
            pass

        try:
            import bluetooth
            bluetooth.BLE().active(False)
            print("Bluetooth disabled")
        except (ImportError, AttributeError, Exception):
            pass
    except Exception as e:
        print(f"Error disabling wireless: {e}")
