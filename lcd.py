from machine import Pin, SPI
import framebuf

# LCD Pin definitions
PIN_LCD_DC = 8
PIN_LCD_CS = 9
PIN_LCD_CLK = 10
PIN_LCD_DIN = 11
PIN_LCD_RST = 12
PIN_LCD_BL = 13


class LCD(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 320
        self.height = 240

        self.chip_select = Pin(PIN_LCD_CS, Pin.OUT)
        self.chip_select(1)

        self.reset = Pin(PIN_LCD_RST, Pin.OUT)

        self.backlight = Pin(PIN_LCD_BL, Pin.OUT)
        self.backlight(0)

        self.spi = SPI(
            1,
            100000_000,
            polarity=0,
            phase=0,
            sck=Pin(PIN_LCD_CLK),
            mosi=Pin(PIN_LCD_DIN),
            miso=None,
        )

        self.data_command = Pin(PIN_LCD_DC, Pin.OUT)
        self.data_command(1)

        self.buffer = bytearray(self.height * self.width * 2)

        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)

        self.init_display()

        self.RED = 0x001F      # Blue bits used for Red
        self.GREEN = 0x07E0    # Green stays the same (middle bits)
        self.BLUE = 0xF800     # Red bits used for Blue
        self.WHITE = 0xFFFF    # All bits set (white is white)
        self.BLACK = 0x0000    # All bits off (black is black)
        self.YELLOW = 0x07FF   # Green + Red (0x07E0 + 0x001F)
        self.CYAN = 0xFFE0     # Green + Blue (0x07E0 + 0xF800)
        self.MAGENTA = 0xF81F  # Red + Blue (0x001F + 0xF800)
        self.DARK_GRAY = 0x4208
        self.LIGHT_GRAY = 0xC618
        self.ORANGE = 0x051F   # Red + some Green
        self.PURPLE = 0x8010   # Red + some Blue
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

        self.write_cmd(0x36)
        self.write_data(0xA0)  # BGR565 Colours

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