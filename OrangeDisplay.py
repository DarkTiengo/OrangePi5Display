# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import psutil
import socket
from time import sleep
from luma.oled.device import ssd1306
from luma.core.render import canvas
from luma.core.interface.serial import i2c
import mdstat

device1 = None
storage_main = None

device2 = None
storage_data1 = None
storage_data2 = None

raid = None
md = None
ndevices = None

def get_network_info():
    conection = psutil.net_if_addrs()
    net_info = {}
    for interface_name, interface_addresses in conection.items():
        for address in interface_addresses:
            if address.family == socket.AF_INET:
                if not address.address.startswith('127.'):
                    net_info[interface_name] = address.address
    return net_info if net_info else None

def get_raid_data():
    try:
        raid_status = mdstat.parse()
        if raid_status['devices'][md]['status']['non_degraded_disks'] == int(ndevices):
            for dev in raid_status['devices'][md]['status']['synced']:
                if dev is not True:
                    return False
            return True
        else:
            return False
    except NotADirectoryError:
        return False
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
            if 'storage2' in datas and 'health' not in datas:
                storage_data2 = datas['storage2']
        
        if 'health' in datas:
          global raid
          global md
          global ndevices
          raid = True
          md = datas['md']
          ndevices = datas['number_of_disks']
            
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
            if raid is not None:
                health = get_raid_data() 
                if health is True:
                    draw.text((5,30),f"RAID OK",fill="white")
                else:
                    draw.text((5,30),f"RAID PROBLEMS",fill="white")
            network_info = get_network_info()
            if network_info:
                for interface, ip in network_info.items():
                    if interface == "eth0":
                        draw.text((5,40),f"IP: {ip}",fill="white")
            else:
                draw.text((5,40),f"IP: OFFLINE",fill="white")
            
    sleep(1)
