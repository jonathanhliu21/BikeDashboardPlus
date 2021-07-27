#!/bin/bash

set -e;

# cd into directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )";
cd $DIR;

# init venv
source env/bin/activate

# start python program
python3 .;

# deactivate venv if out of program
deactivate;
