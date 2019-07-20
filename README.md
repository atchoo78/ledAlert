# LED Alert

Lightweight HTTP server in Python, configured to receive text data via GET/POST and displaying it on a MAX7219 compatible scrolling LED display connected to a Raspberry Pi.

Dependencies:
https://github.com/rm-hull/luma.led_matrix

# Usage

#### HTTP/GET (Web browser):

 `http://raspberrypi.local:8181/?led=1&msg=Hello World!`

#### HTTP/POST (CURL)

```bash
curl -d 'Hello World!' raspberrypi.local:8181/led
```

--   

# Installation

1. First, install the Luma LED display drivers. Follow the installation instructions provided here:
https://github.com/rm-hull/luma.led_matrix

2. Create a new directory in your home folder on the Raspberry Pi, and copy ledAlert.py to it.

```bash
mkdir ~/ledAlert
```

3. Configure it to run as a service on startup
(Feel free to use any text editor of your choice):

```bash
cd /lib/systemd/system/
sudo pico ledAlert.service
```

### Paste or write the following into "ledAlert.service" (the blank file that you just created):

```
[Unit]
Description=LED Alert
After=multi-user.target
 
[Service]
Type=simple
ExecStart=/usr/bin/python /home/YourUsername/ledAlert.py
Restart=on-abort
 
[Install]
WantedBy=multi-user.target 
```
#### Important: Change "YourUsername" (line 7 above) to your actual logon user name (e.g. "/home/pi/ledAlert.py")

```bash
sudo chmod 644 /lib/systemd/system/ledAlert.service
chmod +x /home/YourUsername/ledAlert.py
```
#### Change the user name reference in line 2 (above) as well
```bash
sudo systemctl daemon-reload
sudo systemctl enable ledAlert.service
sudo systemctl start ledAlert.service
```

To check the status of the ledAlert service (or any other system service, for that matter):

```bash
sudo systemctl status ledAlert.service
```



4.```sudo reboot now```
