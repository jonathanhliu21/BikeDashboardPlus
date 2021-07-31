# Updating your Bike Dashboard

By updating, you are deleting and re-installing Bike Dashboard in the same directory. 

1. `ssh` into your pi: 
    ```
    ssh pi@your.pi.ip
    ```
2. `cd` into your BikeDashboardPlus directory, then `cd` into the parent directory (by typing `cd ..`). You can check the Bike Dashboard directory by typing `cat ~/BikeDashboardPlus.txt`
3. Delete the `BikeDashboardPlus.txt` file in the home folder:
    ```
    rm ~/BikeDashboardPlus.txt
    ```
4. Download the install script and run it. Make sure to plug in your Arduino and remember the path of the Arduino port ([How to know what port your Arduino is](./make_yourself.md); go to "Installing").

    Downloading the script:
    ```
    curl -sO https://raw.githubusercontent.com/jonyboi396825/BikeDashboardPlus/master/install.bash 
    ```

    Running it:

    ```
    bash install.bash /dev/port
    ```

    There is no need to remove the Bike Dashboard directory because the install script automatically does that.

5. Wait for it to install, then reboot your Pi:
    ```
    sudo reboot
    ```

6. After rebooting, you will have an updated version of BikeDashboardPlus.
