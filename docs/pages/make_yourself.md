# Making this project yourself
[Back to README](/README.md)

This page is for people who are interested in making a Bike Dashboard with their own Raspberry Pi. The schematics and designs shown are what works best for me and my bike and may not work for you, so feel free to edit the code, the schematics, and the design for the case and mount. 

## Parts needed

## Schematic
![bd_schematic.png](../img/bd_schematic.png)

I did not design a PCB for this schematic. Instead, I soldered all of these components onto a prototype PCB, which was hard and time-consuming. I may design a custom PCB if I come back to this project.

## 3D Printing

More information on 3D Printing and the case/mount design can be found [here](https://github.com/jonyboi396825/BikeDashboardPlus/tree/master/hardware/models).

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
    curl -sO https://raw.githubusercontent.com/jonyboi396825/BikeDashboardPlus/master/install.bash
    ```

    After running this, you will have to figure out the serial port of your Arduino. Type `ls -l /dev` to see all serial ports. The port for the Arduino should be `ttyUSB*` or `ttyACM*`. The best way to check which port the Arduino is located on is to plug in the Arduino, take note of the ports that are `ttyUSB*` or `ttyACM*`, then unplug the Arduino, and see which of those ports disappeared. That port would be the Arduino.

    After getting the path to the serial port (ex `/dev/ttyUSB0` or `/dev/ttyACM0`), type this command in:
    
    ```
    bash install.bash /dev/port
    ```
    Replace `/dev/port` with the actual path to the serial port. The installation process should take around 1-2 minutes on a Raspberry Pi 4 and around 8-10 minutes on a Raspberry Pi Zero.

2. Make a backup of /etc/rc.local: `sudo cp /etc/rc.local /etc/rc_backup.local`
3. Edit /etc/rc.local
- Type `sudo nano /etc/rc.local`
- Scroll down. Type in `bash /path/to/BikeDashboardPlus/run.bash &` **before the** `exit 0`. You can find out the path by typing `cat ~/BikeDashboardPlus.txt`. **Make sure to add the ampersand or the Pi will not boot.** This line will make the Raspberry Pi run the program when it boots.
- Save and exit: Press ^X (Control-X), and then Y, then enter.

![rc_local_edit.png](../img/rc_local_edit.png)

4. Reboot the Pi: `sudo reboot`

From now on, the program should immediately run whenever you turn on and boot up your Raspberry Pi.

## Disabling
This prevents the program from running whenever you start up your Raspberry Pi.

1. Type `sudo nano /etc/rc.local`
2. Delete the line that you added when installing (shown in the image above).
3. Save and exit: Press ^X (Control-X), and then Y, then enter.
4. Reboot the Pi: `sudo reboot`.

To re-enable it, just type that line back into `/etc/rc.local` at the same place.
    
## Uninstalling

1. Disable the program (See "Disabling")
2. `cd` into the directory you installed BikeDashboardPlus in.
- You can check by typing `cat ~/BikeDashboardPlus.txt`
3. Type `rm -rf BikeDashboardPlus` to delete the folder and all of its contents.
4. Type `rm ~/BikeDashboardPlus.txt`
5. Reboot the Pi: `sudo reboot`
