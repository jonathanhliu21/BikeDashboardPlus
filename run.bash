#!/bin/bash

set -e;

# run the python program
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )";

echo "Since the python program will start every time you launch bash, the dashboard will stop working now. 
To prevent this, remove the lines '# Bike Dashboard' and 'source $DIR/run.bash' at the bottom of ~/.bashrc (nano ~/.bashrc or vi ~/.bashrc).
Then, reboot the Raspberry Pi.
To uninstall this, delete this folder (rm -rf $DIR), then delete the two lines mentioned above in ~/.bashrc."

cd $DIR;
python3 .;

