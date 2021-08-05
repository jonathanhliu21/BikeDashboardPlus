# Updating your Bike Dashboard

By updating, you are syncing your local main branch with the Github master branch.

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
    Note that this command will not work if you have uncommitted changes.

4. Reboot your Pi:
    ```
    sudo reboot
    ```
