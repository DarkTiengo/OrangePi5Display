# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import psutil
from time import sleep
from luma.oled.device import ssd1306
from luma.core.render import canvas
from luma.core.interface.serial import i2c

device1 = None
storage_main = None

device2 = None
storage_data1 = None
storage_data2 = None



def get_display_data():
    try:
        with open("/usr/local/etc/display_datas.conf", "r") as file:
            l1 = [linha.strip() for linha in file if not linha.startswith("#")]
            linhas = list(filter(None,l1))
            datas = {}

            for linha in linhas:
                key, value = linha.split('=', 1)
                datas[key] = value
            file.close()

        if 'port1' in datas:
            global device1
            global storage_main
            serial1 = i2c(port=int(datas['port1']), address=datas['address1'])
            device1 = ssd1306(serial1, rotate=int(datas['rotation1']))
            storage_main = datas['main']

        if 'port2' in datas:
            global device2
            global storage_data1
            global storage_data2
            serial2 = i2c(port=int(datas['port2']),address=datas['address2'])
            device2 = ssd1306(serial2,rotate=int(datas['rotation2']))
            if 'storage1' in datas:
                storage_data1 = datas['storage1']
            if 'storage2' in datas:
                storage_data2 = datas['storage2']
        file.close()
    except FileNotFoundError:
        raise FileNotFoundError("Conf File is not Found")

def get_orange_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
            temperature_str = file.read().strip()
            temperature_celsius = int(temperature_str) / 1000.0
            return temperature_celsius
    except FileNotFoundError:
        return None


get_display_data()
while True:
    OrangeTemp = get_orange_temp()
    if device1 is not None:
        with canvas(device1) as draw:
            draw.text((5, 2), "Tiengo NAS V1.0", fill="white")
            draw.text((5, 20), f"CPU: {psutil.cpu_percent()} %", fill="white")
            draw.text((5, 30),
                      f"Mem. Usada: {psutil.virtual_memory().used / (1024 ** 3):.1f}/"
                      f"{psutil.virtual_memory().total / (1024 ** 3):.1f} GB",
                      fill="white")
            draw.text((5, 40), f"Esp Usado: {psutil.disk_usage(storage_main).percent} %", fill="white")
            if OrangeTemp is not None:
                draw.text((5, 50), f"Temp: {OrangeTemp:.2f} C", fill="white")
    if device2 is not None:
        with canvas(device2) as draw:
            draw.text((5,2),"Armazenamento:",fill="white")
            if storage_data1 is not None:
                draw.text((5,20),f"Arm 1: {psutil.disk_usage(storage_data1).used / (1024 ** 3):.1f}/"
                                f"{psutil.disk_usage(storage_data1).total / (1024 ** 3):.1f} GB", fill="white")
            if storage_data2 is not None:
                draw.text((5,30),f"Arm 2: {psutil.disk_usage(storage_data2).used / (1024 ** 3):.1f}/"
                                f"{psutil.disk_usage(storage_data2).total / (1024 ** 3):.1f} GB", fill="white")
    sleep(1)
