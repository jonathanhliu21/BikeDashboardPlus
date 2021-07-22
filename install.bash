#!/bin/bash

set -e;

start=$SECONDS;

if [[ "$1 " == " " ]];
    then
    echo "Need path to Arduino serial port (ex: /dev/ttyUSB0).";
    exit 1;
fi;

read -p "This will install BikeDashboardPlus on your current directory. From now on, __main__.py will be activated when bash activates. If bash is not your default shell, type in 'chsh -s /bin/bash/'. Make sure you have your Arduino plugged in before continuing. Continue? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1;

if (cat /proc/device-tree/model | grep -q "Raspberry Pi");
    then 
    cp install.bash install_backup.bash;

    # check if Bike Dashboard is already installed elsewhere
    if grep -q "Bike Dashboard" ~/.bashrc;
        then
        echo "Bike Dashboard already installed. Check ~/.bashrc to see where.";
        exit 1;
    fi;

    # remove file
    rm -rf BikeDashboardPlus || true;

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
    if (git clone https://github.com/jonyboi396825/BikeDashboardPlus.git && rm -rf BikeDashboardPlus/.git);
        then
        rm BikeDashboardPlus/install.bash || true;
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

    # add tracking folder
    mkdir BikeDashboardPlus/tracking; 

    # add cfg.json with default cfg 
    touch BikeDashboardPlus/raspberrypi/cfg.json;
    printf "{\"LED\": 0, \"DTM\": 0, \"TMZ\": \"UTC\", \"UNT\": 0, \"24H\": 0}\n" >> BikeDashboardPlus/raspberrypi/cfg.json;

    # add USB port to port file
    touch BikeDashboardPlus/raspberrypi/port;
    printf "$1" >> BikeDashboardPlus/raspberrypi/port;

    # edit .bashrc so it source calls run.bash on startup.
    # Copies bashrc. When installing, it will mv bashrc_backup to bashrc, replacing bashrc's contents with bashrc_backup's
    cp ~/.bashrc ~/.bashrc_backup;
    
    # Adds script to run program into .bashrc so the program runs whenever bash starts up.
    printf "# Bike Dashboard \n" >> ~/.bashrc;  
    printf "source $PWD/BikeDashboardPlus/env/bin/activate \n" >> ~/.bashrc;
    printf "source $PWD/BikeDashboardPlus/run.bash \n" >> ~/.bashrc;

    duration=$(( SECONDS - start ));
    echo "Installation finished in $duration seconds. Reboot the pi to let it take effect. Now deleting install.bash.";

    # remove itself
    rm -- "$0";

else 
    echo "Installation failed: You are not on a Raspberry Pi";
    exit 1;
fi;
