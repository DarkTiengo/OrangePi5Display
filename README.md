# OrangePi5Display

A simple Python script to operate an SSH1306 LED display with system information, running on an Orange Pi 5. Other Orange Pi don't tested.


## Install 

Plug the display in i2c ports 3 and 5 of the Orange Pi.

### Armbian

``` console
sudo armbian-config
```

### Ubuntu and Debian

``` console
sudo orangepi-config
```

Go to System->Hardware and mark i2c3-m0 and i2c5-m3 and reboot. Paste de code:

```console
wget -O - https://raw.githubusercontent.com/DarkTiengo/OrangePi5Display/master/install.sh | bash

```
