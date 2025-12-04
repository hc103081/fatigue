from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import ImageDraw, ImageFont, Image
import time

def clear_oled(device):
    image = Image.new('1', (device.width, device.height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, device.width, device.height), fill=0)
    device.display(image)

serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

# 載入中文字型
font = ImageFont.truetype("/usr/share/fonts/truetype/arphic/ukai.ttc", 16)  # 路徑與字型大小可調整

image = Image.new('1', (device.width, device.height))
draw = ImageDraw.Draw(image)
draw.text((1, 1), "陪騎是給！", font=font, fill=255)
device.display(image)

while True:
    time.sleep(1)