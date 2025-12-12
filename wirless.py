import network


def disable():
    """Disable WiFi and Bluetooth on Pico W/2W to save power."""
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(False)

        try:
            import bluetooth

            bluetooth.BLE().active(False)
        except (ImportError, AttributeError):
            pass
    except Exception as e:
        print(f"Error disabling wireless: {e}")
