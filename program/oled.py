import time
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont

# Raspberry Pi pin configuration
RST = None  # on PiOLED this pin isn't used

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Load default font.
font = ImageFont.load_default()

# Write some text
draw.text((0, 0), 'Hello, Raspberry Pi!', font=font, fill=255)

# Display image.
disp.image(image)
disp.display()

time.sleep(2)