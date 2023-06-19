#!/bin/bash
# create bash script to crete python virtual environment and install required packages
# create virtual environment
python3 -m venv venv

# activate virtual environment
source venv/bin/activate

# install required packages
pip install -r requirements.txt

# run the app
python3 main.py
