# pizcamhd
Raspberry Pi HDMI webcam with HTML control interface

## Setup

1) Update `sudo apt-get update`
2) Upgrade `sudo apt-get upgrade`
3) Install git `sudo apt-get install git`
4) Install pip `sudo apt install python3-pip`
5) Install python3 `sudo apt-get install python3`
6) Clone this repository `git clone https://github.com/marclura/pizcamhd.git`
7) Install picamera `sudo apt-get install python3-picamera`
8) Install netifaces `sudo pip3 install netifaces`
9) Install Flask `sudo pip install Flask`

## Activate the camera port

1) Enter the Raspberry Pi configurations `sudo raspi-config`
2) Enter the `3 Interface Options`
3) Select the `I1 Legacy Camera` and confirm with `<Yes>` when asked if you woud like to enable it
4) Select `<Finish>` and confirm the reboot for the configuration to take place

## Run it for testing

1) Enter the folder `cd pizcamhd`
2) Run the python script `sudo python3 pizcamhd.py`
3) Press `CTRL+C` to stop and close the script

## Run it automatically at boot

1) Set the python script as executable `sudo chmod +x pizcamhd.py`
2) Add the script to the rc.list to run it at boot `sudo nano /etc/rc.local`
3) Add this line of code just before the "exit 0" line (change PI_NAME with your current local user) `sudo python3 /home/PI_NAME/pizcamhd/pizcamhd.py &`
4) Close the nano text editor with the keys `CTRL+X` and confrim with the key `Y` to save the modification on the file
5) Restart the Raspberry Pi to check if everything worked out ok `sudo reboot`
