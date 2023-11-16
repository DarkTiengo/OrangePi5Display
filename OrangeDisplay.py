# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import psutil
from time import sleep
from luma.oled.device import ssd1306
from luma.core.render import canvas
from luma.core.interface.serial import i2c

serial = i2c(port=5, address=0x3c)
device = ssd1306(serial, rotate=0)


def get_orange_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
            temperature_str = file.read().strip()
            temperature_celsius = int(temperature_str) / 1000.0
            return temperature_celsius
    except FileNotFoundError:
        return None


while True:
    OrangeTemp = get_orange_temp()
    with canvas(device) as draw:
        draw.text((5, 2), "Tiengo NAS V1.0", fill="white")
        draw.text((5, 20), f"CPU: {psutil.cpu_percent()} %", fill="white")
        draw.text((5, 30),
                  f"Mem. Usada: {psutil.virtual_memory().used / (1024 ** 3):.1f}/"
                  f"{psutil.virtual_memory().total / (1024 ** 3):.1f} GB",
                  fill="white")
        draw.text((5, 40), f"Esp Usado: {psutil.disk_usage('/').percent} %", fill="white")
        if OrangeTemp is not None:
            draw.text((5, 50), f"Temp: {OrangeTemp:.2f} C", fill="white")
    sleep(1)
