sudo apt update && sudo apt install git swig python3-dev python3-setuptools python3-pip libgpiod-dev -y

git clone --recursive https://github.com/orangepi-xunlong/wiringOP-Python -b next
cd wiringOP-Python
python3 generate-bindings.py > bindings.i
python3 setup.py install

usermod $USER -aG i2c

cd /tmp
git clone https://github.com/DarkTiengo/OrangePi5Display.git
cd OrangePi5Display
pip install -r requeriments.txt
cp OrangeDisplay.py /usr/bin
cp display_datas.conf /usr/local/etc
cd ..
rm -r OrangePi5Display

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

systemctl daemon-reload
systemctl enable OrangePi5Display.service
systemctl start OrangePi5Display.service

cd -

echo "Installation Complete."
