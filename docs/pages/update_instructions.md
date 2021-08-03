# Updating your Bike Dashboard

By updating, you are deleting and re-installing Bike Dashboard in the same directory. 

1. `ssh` into your pi: 
    ```
    ssh pi@your.pi.IP
    ```

2. `cd` into your BikeDashboardPlus directory. You can check the Bike Dashboard directory by typing `cat ~/BikeDashboardPlus.txt` 

3. Run this command (it syncs the code on the master branch on Github with the code on your local Pi):
    ```
    git pull --rebase origin master
    ```
    This will not delete your tracking or error files because they were put inside `.gitignore` when installing.

4. Reboot your Pi:
    ```
    sudo reboot
    ```