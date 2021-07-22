# Making this project yourself
[Back to README](/README.md)

## Parts needed

## Schematic
![bd_schematic.png](../img/bd_schematic.png)


## 3D Printing

## Installation

There will be two steps during installation: configuring your Pi so the software will work, and actually installing the software. However, before that:

If you haven't installed the Raspberry Pi OS, follow the instructions below. Make sure to install "Raspberry Pi OS (32 bit)" and not any other OS as they might not come with Python or cURL.
- [Setting up the Raspberry Pi](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up)
- [Setting up the Raspberry Pi headless](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md)

- Python installation if you do not have it installed
  ```
  sudo apt update
  sudo apt install python3 idle3
  ```

- Curl installation if you do not have it installed:
  ```
  sudo apt update
  sudo apt install curl
  ```

### Configuring

1. Type in `sudo raspi-config`
2. Go to "Interface options" and select `I2C`, then select Yes.
3. Return to "Interface options" and select `Serial Port`. When it asks `Would you like a login shell to be accessible over serial?`, select No. It will then ask, `Would you like the serial port hardware to be enabled?`, and select Yes.
4. Click Finish.
5. Reboot the Raspberry Pi: `sudo reboot`

### Installing

1. To install BikeDashboard Plus, first run this command: 
    ```
    curl -s https://raw.githubusercontent.com/jonyboi396825/BikeDashboardPlus/master/install.bash -o install.bash
    ```

    After running this, you will have to figure out what serial port your Arduino. Type `ls -l /dev` to see all serial ports. The port for the Arduino should be `ttyUSB*` or `ttyACM*`. The best way to check which port the Arduino is located on is to plug in the Arduino, take note of the ports that are `ttyUSB*` or `ttyACM*`, then unplug the Arduino, then see which of those ports disappeared. That port would be the Arduino.

    After getting the path to the serial port (ex `/etc/ttyUSB0` or `/etc/ttyACM0`), type this command in:
    
    ```
    bash install.bash /path/to/serial/port
    ```
    Replace `/path/to/serial/port` with the actual path to the serial port.

    **This will edit ~/.bashrc, running the program whenever you start bash, so if you start the terminal, make sure to type ^C (control-C) to exit out of the program.**

2. Make a backup of /etc/rc.local: `sudo cp /etc/rc.local /etc/rc_backup.local`
3. Edit /etc/rc.local
- Type `sudo nano /etc/rc.local`
- Scroll down. Type in `bash &` on the line that is before `exit 0`. **Make sure you type it before** `exit 0` **, and you type in the ampersand (&) or the Pi will not boot.**
- Save and exit: Press ^X (Control-X), and then Y.

![rc_local_edit.png](../img/rc_local_edit.png)

4. Reboot the Pi: `sudo reboot`

From now on, the program should immediately run whenever you turn on and boot up your Raspberry Pi.

## What if I want to open my terminal? (Disabling) 
This prevents the program from running whenever you start up your terminal on your Raspberry Pi.

1. When you open the terminal, press ^C (Control-C) **immediately**.
2. Run this command: `nano ~/.bashrc`
3. Scroll down and remove the following lines from ~/.bashrc.
```bash
# Bike Dashboard 
source /path/to/BikeDashboardPlus/run.bash
```

![bashrc_edit.png](../img/bashrc_edit.png)

4. Press ^X (Control-X), then Y to save and exit.
5. Reboot the Pi: `sudo reboot`
    
## Uninstalling

1. Disable the program (See "Disabling")
2. Remove the `bash` command from /etc/rc.local by typing in `sudo nano /etc/rc.local`
3. Delete the `bash &` line you wrote when installing.
4. Save and exit (Press ^X then Y)
5. `cd` into the directory you installed BikeDashboardPlus in.
6. Type `rm -rf BikeDashboardPlus` to delete the folder and all of its contents.
7. Reboot the Pi: `sudo reboot`
