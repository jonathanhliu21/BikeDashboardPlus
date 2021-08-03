#!/bin/bash


# MIT License

# Copyright (c) 2021 jonyboi396825

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

set -e;

start=$SECONDS;

if [[ "$1 " == " " ]];
    then
    echo "Need path to Arduino serial port (ex: /dev/ttyUSB0).";
    exit 1;
fi;

read -p "This will install BikeDashboardPlus on your current directory (~ 29 megabytes). Make sure you have your Arduino plugged in before continuing. Continue? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 0;

if (cat /proc/device-tree/model | grep -q "Raspberry Pi");
    then 

    # check if Bike Dashboard is already installed elsewhere
    if ( v=$(find ~ -maxdepth 1 -iname "BikeDashboardPlus.txt"); ! [ "$v" = "" ] );
        then
        bdpath=$(<~/BikeDashboardPlus.txt);
        echo "Bike Dashboard already installed in $bdpath";
        exit 0;
    fi;

    # remove file
    rm -rf BikeDashboardPlus || true;

    # check if port exists
    if ( v=$(find /dev -maxdepth 1 -wholename "$1"); [ "$v" = "" ] || ( ! [[ "$1" = "/dev/"* ]] ) );
        then
        echo "Port not found";
        exit 1;
    fi;

    # install GPS libraries
    echo "Installing GPS libraries...";
    if (yes | sudo apt install minicom gpsd gpsd-clients);
        then
        echo "Done installing GPS libraries.";
    else
        echo "Installing failed: Failed to install GPS libraries";
        exit 1;
    fi;

    # disable gpsd.socket
    sudo systemctl disable gpsd.socket;

    # clone repository
    echo "Cloning repository...";
    if (git clone https://github.com/jonyboi396825/BikeDashboardPlus.git);
        then
        echo "Cloned code repository.";
    else
        echo "Installation failed: Failed to clone repository.";
        exit 1;
    fi;

    # init venv
    echo "Initializing virtualenv...";
    if (python3 -m venv BikeDashboardPlus/env);
        then
        source BikeDashboardPlus/env/bin/activate;
        echo "Successfully initiated venv.";
    else
        echo "Could not initiate venv.";
        exit 1;
    fi;

    # pip3 install
    echo "Installing needed libraries...";
    if (pip3 install Adafruit-SSD1306 Adafruit_BBIO gps pytz RPi.GPIO pyserial pillow flask gpiozero requests);
        then 
        echo "Finished installing libraries.";
    else
        echo "Installation failed: failed to install libraries.";
        exit 1;
    fi;

    # install arduino-cli
    echo "Installing Arduino-CLI...";
    mkdir BikeDashboardPlus/bin;
    curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=BikeDashboardPlus/bin sh;

    # install boards
    echo "Installing Arduino-CLI avr board (Nano)...";
    BikeDashboardPlus/bin/arduino-cli core install arduino:avr;
    echo "Successfully installed Arduino Nano.";

    echo "Installing Arduino libraries...";
    BikeDashboardPlus/bin/arduino-cli lib install ArduinoJson;
    echo "Done installing libraries.";

    # arduino-cli compile & upload code to Arduino
    echo "Compiling and uploading code to Arduino...";
    if (BikeDashboardPlus/bin/arduino-cli compile --fqbn arduino:avr:nano BikeDashboardPlus/arduino/BikeDashboardPlus && BikeDashboardPlus/bin/arduino-cli upload -p $1 --fqbn arduino:avr:nano BikeDashboardPlus/arduino/BikeDashboardPlus);
        then
        echo "Successfully compiled and uploaded code to Arduino.";
    else
        echo "Failed to compile code to Arduino, perhaps you entered the port wrong?";
        exit 1;
    fi;

    # remove arduino-cli in case of conflict
    rm -rf BikeDashboardPlus/bin

    # add gitignore
    mv BikeDashboardPlus/ignored_files.txt BikeDashboardPlus/.gitignore

    # add tracking folder
    mkdir BikeDashboardPlus/tracking; 

    # add cfg.json with default cfg 
    touch BikeDashboardPlus/raspberrypi/cfg.json;
    printf "{\"LED\": 0, \"DTM\": 0, \"TMZ\": \"UTC\", \"UNT\": 0, \"24H\": 0}\n" >> BikeDashboardPlus/raspberrypi/cfg.json;

    # add USB port to port file
    touch BikeDashboardPlus/raspberrypi/port;
    printf "$1" >> BikeDashboardPlus/raspberrypi/port;

    # put BikeDashboardPlus in home folder to indicate that it was installed
    touch ~/BikeDashboardPlus.txt
    echo "$PWD/BikeDashboardPlus" >> ~/BikeDashboardPlus.txt;

    duration=$(( SECONDS - start ));
    echo "Installation finished in $duration seconds. Now deleting install.bash.";

    # remove itself
    rm -- "$0";

else 
    echo "Installation failed: You are not on a Raspberry Pi";
    exit 1;
fi;
