sudo apt update && sudo apt install git swig python3-dev python3-setuptools python3-pip libgpiod-dev -y

git clone --recursive https://github.com/orangepi-xunlong/wiringOP-Python -b next
cd wiringOP-Python
python3 generate-bindings.py > bindings.i
sudo python3 setup.py install


arquivo="/etc/udev/rules.d/99-rk-device-permissions.rules"
echo 'SUBSYSTEM=="i2c-dev", GROUP="i2c", MODE="0666"' | sudo tee -a "$arquivo" > /dev/null

cd /tmp
git clone https://github.com/DarkTiengo/OrangePi5Display.git
cd OrangePi5Display
python3-pip install -r requeriments.txt
sudo cp OrangeDisplay.py /usr/bin
sudo cp display_datas.conf /usr/local/etc
cd ..
sudo rm -r OrangePi5Display

cat <<EOF | sudo tee /etc/systemd/system/OrangePi5Display.service
[Unit]
Description=Oled Display System Information
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python3 /usr/bin/OrangeDisplay.py

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable OrangePi5Display.service
sudo systemctl start OrangePi5Display.service

cd -

echo "Installation Complete."
