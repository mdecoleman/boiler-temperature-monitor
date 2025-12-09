# Boiler Temperature Monitor

A Raspberry Pi Pico W-based temperature monitoring system for tracking flow, return, and hot water temperatures on older boilers without digital gauges.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi%20Pico%20W-red.svg)
![Python](https://img.shields.io/badge/python-MicroPython-green.svg)

## 📋 Project Overview

This project adds digital temperature monitoring to older boilers that lack built-in temperature displays. Using three DS18B20 waterproof temperature sensors, it continuously monitors and displays:

- **Flow Temperature** (supply line to radiators)
- **Return Temperature** (return line from radiators)
- **Hot Water Temperature** (domestic hot water)

The system provides a real-time display on an LCD screen with button navigation to view individual sensor readings in detail.

## 🎯 Problem Statement

Many older boilers have:
- ❌ No digital temperature readouts
- ❌ Limited visibility into system performance
- ❌ Difficulty diagnosing heating issues
- ❌ No way to verify optimal operating temperatures

This project solves these problems by adding affordable, real-time temperature monitoring.

## ✨ Features

- **Real-time monitoring** of three temperature sensors
- **LCD display** (320x240 ST7789) with multiple screens
- **Button navigation** to switch between views
- **Home screen** showing all three temperatures at once
- **Detailed screens** for individual sensor readings
- **Color-coded temperatures** (optional, based on thresholds)
- **Low cost** (~$20-30 in parts)
- **Easy installation** - no boiler modifications required
- **Interrupt-driven buttons** for responsive UI
- **Efficient polling** - sensor reads every 5 seconds

## 🛠️ Hardware Requirements

### Core Components

- **Raspberry Pi Pico W** ($6) - Main controller
- **ST7789 LCD Display** (320x240, SPI) ($8-15) - Display module with 4 buttons
- **3x DS18B20 Waterproof Temperature Sensors** ($3-5 each) - OneWire digital sensors
- **4.7kΩ Resistor** (for OneWire bus pull-up)
- **Micro USB cable** (for power)
- **Jumper wires** / breadboard for prototyping

### Optional
- **Enclosure** for mounting near boiler
- **Power supply** (5V USB adapter)
- **Heat-resistant wire** if routing near hot pipes

## 📐 Wiring Diagram

```
Raspberry Pi Pico W Connections:

LCD Display (ST7789 - SPI):
├─ DC    → GPIO 8
├─ CS    → GPIO 9
├─ CLK   → GPIO 10
├─ DIN   → GPIO 11
├─ RST   → GPIO 12
├─ BL    → GPIO 13
├─ VCC   → 3.3V
└─ GND   → GND

Buttons:
├─ Top Left     → GPIO 2
├─ Top Right    → GPIO 3
├─ Bottom Left  → GPIO 17
└─ Bottom Right → GPIO 15

Temperature Sensors (DS18B20 - OneWire):
├─ Data  → GPIO 18 (with 4.7kΩ pull-up to 3.3V)
├─ VCC   → 3.3V (or 5V if using parasitic power)
└─ GND   → GND

OneWire Bus:
  All three DS18B20 sensors connect in parallel to GPIO 18
  Single 4.7kΩ resistor between Data line and 3.3V
```

### DS18B20 Sensor Wire Colors
```
Red    → VCC (3.3V or 5V)
Black  → GND
Yellow → Data (GPIO 18)
```

## 📦 Software Setup

### Prerequisites

- [MicroPython](https://micropython.org/download/RPI_PICO_W/) firmware installed on Pico W
- [Thonny IDE](https://thonny.org/) or similar for uploading files
- Python for initial setup

### Installation

1. **Flash MicroPython to Pico W**
   ```bash
   # Download latest MicroPython firmware for Pico W
   # Hold BOOTSEL button while plugging in USB
   # Drag .uf2 file to RPI-RP2 drive
   ```

2. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/boiler-temp-monitor.git
   cd boiler-temp-monitor
   ```

3. **Upload files to Pico**
   
   Upload these files to the Pico using Thonny or mpremote:
   ```
   main.py       - Main application loop
   lcd.py        - LCD display driver
   buttons.py    - Button handler with debouncing
   ```

4. **Configure sensor IDs**
   
   Run the project once to see sensor IDs in console output:
   ```python
   # Console output will show:
   Sensor 1: 25.5°C, ID: 0xb20b2551d0e81428
   Sensor 2: 30.2°C, ID: 0xb10b2551cf9fc728
   Sensor 3: 22.8°C, ID: 0x460b2551a7326c28
   ```
   
   Update `SENSORS_MAP` in `main.py` with your sensor IDs:
   ```python
   SENSORS_MAP = {
       "temp_1": {"id": "0xYOUR_SENSOR_1_ID", "name": "Flow Temp"},
       "temp_2": {"id": "0xYOUR_SENSOR_2_ID", "name": "Return Temp"},
       "temp_3": {"id": "0xYOUR_SENSOR_3_ID", "name": "Hot Water"},
   }
   ```

5. **Mount sensors on boiler**
   
   Attach sensors to pipes using:
   - Pipe clamps or zip ties
   - Thermal paste for better contact
   - Insulation over sensors for accuracy

## 🎮 Usage

### Button Controls

- **Top Left** - Cycle through screens (Home → Sensor 1 → Sensor 2 → Sensor 3 → Home)
- **Top Right** - *(Not currently assigned)*
- **Bottom Left** - *(Not currently assigned)*
- **Bottom Right** - *(Not currently assigned)*

### Screen Views

**Home Screen** - All three temperatures displayed
```
┌──────────────────────────┐
│ Flow Temp                │
│ 65.2 C                   │
├──────────────────────────┤
│ Return Temp              │
│ 55.8 C                   │
├──────────────────────────┤
│ Hot Water                │
│ 48.3 C                   │
└──────────────────────────┘
```

**Individual Sensor Screens** - Detailed view of single sensor

## 🔧 Configuration

### Adjust Update Interval

Change sensor reading frequency in `main.py`:
```python
DEFAULT_INTERVAL_SECONDS = 5  # Read sensors every 5 seconds
```

### Customize Temperature Thresholds

Modify color coding in `main.py`:
```python
def get_color_for_temp(lcd, temp):
    if temp > 70:
        return lcd.RED      # Too hot
    elif temp > 65:
        return lcd.YELLOW   # Warm
    elif temp < 55:
        return lcd.BLUE     # Cool
    else:
        return lcd.WHITE    # Normal
```

### Button Debounce Time

Adjust button responsiveness in `buttons.py`:
```python
self.debounce_ms = 200  # 200ms debounce (increase if double-pressing)
```

## 📊 Typical Operating Temperatures

| Measurement | Normal Range | Notes |
|-------------|--------------|-------|
| **Flow** | 60-80°C | Supply to radiators |
| **Return** | 40-60°C | Return from radiators |
| **Delta** | 10-20°C | Flow - Return difference |
| **Hot Water** | 50-60°C | Domestic hot water |

*These are general guidelines. Your boiler may operate differently.*

## 🐛 Troubleshooting

### No Sensors Found
- Check wiring: Data to GPIO 18, VCC to 3.3V, GND to GND
- Verify 4.7kΩ pull-up resistor is installed
- Test sensors individually
- Check for loose connections

### Incorrect Temperatures
- Ensure good thermal contact with pipes
- Add thermal paste between sensor and pipe
- Insulate sensors from ambient air
- Verify sensor IDs match in `SENSORS_MAP`

### Screen Not Updating
- Check LCD wiring (especially DC, CS, CLK, DIN pins)
- Verify 3.3V power supply is stable
- Check console output for errors

### Button Presses Not Working
- Verify button GPIO pins match your LCD module
- Check pull-up resistors are enabled
- Increase debounce time if buttons feel unresponsive

### Multiple Screen Changes Per Press
- Buttons are bouncing - debouncing may be disabled
- Increase `debounce_ms` value in buttons.py

## 🏗️ Project Structure

```
boiler-temp-monitor/
├── main.py              # Main application loop
├── lcd.py               # LCD display driver (ST7789)
├── buttons.py           # Button handler with interrupt-based debouncing
├── README.md            # This file
├── docs/
│   └── wiring.md        # Detailed wiring diagrams
└── examples/
    └── test_sensors.py  # Test script to identify sensor IDs
```

## 🎓 How It Works

### System Architecture

1. **Sensor Reading** (OneWire Protocol)
   - Three DS18B20 sensors share one data line (GPIO 18)
   - Each sensor has unique 64-bit ROM ID
   - Sensors polled every 5 seconds
   - Conversion takes ~750ms per cycle

2. **Display Updates** (SPI Communication)
   - ST7789 LCD driven via SPI at 100MHz
   - Screen refreshes when:
     - Sensors are read (every 5 seconds)
     - Screen changes (button press)
   - Efficient: Only redraws when needed

3. **Button Handling** (GPIO Interrupts)
   - Hardware interrupts for instant response
   - Software debouncing (200ms) prevents bounce
   - No polling loop needed - event-driven

4. **Main Loop**
   ```python
   while True:
       check_for_screen_changes()    # 50ms polling
       read_sensors_if_time()        # Every 5 seconds
       update_display_if_needed()
       sleep(0.05)                   # Short sleep for responsiveness
   ```

## 🔬 Technical Details

- **Microcontroller:** RP2040 dual-core ARM Cortex-M0+ @ 133MHz
- **Memory:** 264KB SRAM, 2MB Flash
- **Sensor Protocol:** 1-Wire (Dallas/Maxim)
- **Display Protocol:** SPI (Serial Peripheral Interface)
- **Sensor Accuracy:** ±0.5°C (DS18B20)
- **Temperature Range:** -55°C to +125°C
- **Resolution:** 12-bit (0.0625°C)

## 🚀 Future Enhancements

- [ ] Wi-Fi connectivity for remote monitoring
- [ ] Data logging to SD card or cloud
- [ ] Historical temperature graphs
- [ ] Alarm notifications (email/SMS) for abnormal temps
- [ ] Web dashboard for multi-device monitoring
- [ ] Calculate and display system efficiency
- [ ] Support for additional sensors
- [ ] MQTT integration for home automation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Safety Notice

**IMPORTANT:** This project involves working near heating systems. Please observe these safety precautions:

- ⚠️ Always turn off boiler power before working on pipes
- ⚠️ Be aware of hot surfaces - pipes can exceed 80°C
- ⚠️ Do not modify boiler internals
- ⚠️ Sensors attach externally - no penetration of pipes
- ⚠️ Consult a qualified heating engineer if unsure
- ⚠️ This is a monitoring tool, not a control system
- ⚠️ Do not use for safety-critical applications

## 🙏 Acknowledgments

- MicroPython community for excellent embedded Python support
- Raspberry Pi Foundation for the Pico W
- DS18B20 sensor manufacturers
- ST7789 LCD display library contributors

## 📧 Contact

Project Link: [https://github.com/yourusername/boiler-temp-monitor](https://github.com/yourusername/boiler-temp-monitor)

---

**Enjoying this project?** Give it a ⭐️ on GitHub!