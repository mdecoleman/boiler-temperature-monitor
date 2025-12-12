from constants import (
    LCD_PIN_BL,
    LCD_PIN_CLK,
    LCD_PIN_CS,
    LCD_PIN_DC,
    LCD_PIN_DIN,
    LCD_PIN_RST,
)
from machine import Pin, SPI

import framebuf


class LCD(framebuf.FrameBuffer):
    def __init__(self, rotation=90):
        self.width = 320
        self.height = 240
        self.rotation = rotation

        self.chip_select = Pin(LCD_PIN_CS, Pin.OUT)
        self.chip_select(1)
        self.reset = Pin(LCD_PIN_RST, Pin.OUT)
        self.backlight = Pin(LCD_PIN_BL, Pin.OUT)
        self.backlight(0)
        self.spi = SPI(
            1,
            100000_000,
            polarity=0,
            phase=0,
            sck=Pin(LCD_PIN_CLK),
            mosi=Pin(LCD_PIN_DIN),
            miso=None,
        )
        self.data_command = Pin(LCD_PIN_DC, Pin.OUT)
        self.data_command(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()

        self.RED = 0x001F  # Red in BGR mode
        self.GREEN = 0x07E0  # Green (same in both modes)
        self.BLUE = 0xF800  # Blue in BGR mode
        self.WHITE = 0xFFFF  # White
        self.BLACK = 0x0000  # Black
        self.YELLOW = 0x07FF  # Red + Green in BGR
        self.CYAN = 0xFFE0  # Green + Blue in BGR
        self.MAGENTA = 0xF81F  # Red + Blue in BGR
        self.DARK_GRAY = 0x4208
        self.LIGHT_GRAY = 0xC618
        self.ORANGE = 0x051F  # Red + some Green
        self.PURPLE = 0x8010  # Red + some Blue
        self.PINK = 0x0C1F

    def write_cmd(self, cmd):
        self.chip_select(1)
        self.data_command(0)
        self.chip_select(0)
        self.spi.write(bytearray([cmd]))
        self.chip_select(1)

    def write_data(self, buf):
        self.chip_select(1)
        self.data_command(1)
        self.chip_select(0)
        self.spi.write(bytearray([buf]))
        self.chip_select(1)

    def init_display(self):
        self.backlight(1)
        self.reset(1)
        self.reset(0)
        self.reset(1)

        rotations = {
            0: 0x00,  # Portrait
            90: 0x60,  # Landscape
            180: 0xC0,  # Portrait (180°)
            270: 0xA0,  # Landscape (180°)
        }
        BGR_MODE = 0x08  # BGR color order bit

        self.write_cmd(0x36)
        self.write_data(rotations[self.rotation] | BGR_MODE)

        self.write_cmd(0x3A)
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35)

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F)

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)

        self.write_cmd(0x21)
        self.write_cmd(0x11)
        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x3F)

        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)

        self.write_cmd(0x2C)

        self.chip_select(1)
        self.data_command(1)
        self.chip_select(0)
        self.spi.write(self.buffer)
        self.chip_select(1)

    def clear(self):
        self.fill(self.BLACK)
        self.show()

    def sleep(self):
        self.backlight(0)
        self.clear()

    def wake(self):
        self.backlight(1)
        self.clear()
