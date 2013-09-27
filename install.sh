#! /bin/bash
#
# This script makes check_fits_timestamps executible and copies it to ~/bin.
# This script is only intended for the Argos instrument on hoth.as.utexas.edu

if [ -f check_fits_timestamps.py ]; then
    chmod +x check_fits_timestamps.py
    cp -f check_fits_timestamps.py ~/bin/.
else
    echo "check_fits_timestamps.py does not exist in the current working directory."
    echo "cd to the parent directory of this install script in order to run."
fi

