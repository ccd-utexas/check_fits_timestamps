#! /usr/bin/env python
"""check_fits_timestamps.py

Calls check_fits_timestamps module to compare timestamps between pairs of
subsequent FITS files to check that timestamps are separated by the
exposure time. This program is specific to Argos data.

Example use:
check_fits_timestamps.py /path/to/data/A1234.*.fits
"""
# TODO: Format documentation following
# http://docs.python.org/devguide/documenting.html

import sys
from astropy.io import fits
import time
import datetime

def main():
    """Main code.

    Enters infinte loop calling check_fits_timestamps.

    Arguments:
    None.

    Returns:
    Prints to stdout.
    """
    # Main program is modularized to prevent code execution when being imported.
    stop_instructions = "Hit Ctrl-C to stop program."
    print
    print stop_instructions
    while True:
        check_fits_timestamps()
        print
        print stop_instructions
        sleep_time = 10 # seconds
        print "Sleeping for", sleep_time, "seconds."
        time.sleep(sleep_time)

class bcolors:
    """Class of border colors using ANSI escape sequences.

    Modified from
    http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
    Also see
    http://www.tldp.org/HOWTO/Bash-Prompt-HOWTO/x329.html
    """
    BOLDGREEN = '\033[1;32m'
    BOLDRED   = '\033[1;31m'
    DEFAULT   = '\033[0m'

    def disable(self):
        self.BOLDGREEN = ''
        self.BOLDRED   = ''
        self.DEFAULT   = ''

def check_fits_timestamps():
    """Check timestamps of FITS files for Argos data.

    Compares timestamps between pairs of subsequent FITS files to check that
    timestamps are spaced by the exposure time. This script is specific to
    Argos data.

    Arguments:
    List of FITS files.

    Returns:
    Prints to stdout.
    """
    # FITS files from Argos do not conform to FITS standard:
    # - Actual file length is smaller than expected standard.
    # - Illegal keyword 'NTP:GPS'
    fits_file_list = sys.argv[1:]

    print
    print datetime.datetime.utcnow().isoformat()
    print "Begin checking FITS timestamps for "
    print fits_file_list[0]
    print "..."
    print fits_file_list[-1]
    # Speed of program is ~180 files per second.
    print "Runtime estimate:", len(fits_file_list)/180, "seconds"

    flag_no_timing_errors = True
    old_fits_file  = fits_file_list[0]
    hdulist        = fits.open(old_fits_file)
    old_exptime    = float(hdulist[0].header['EXPTIME'])
    old_unixtime   = float(hdulist[0].header['UNIXTIME'])
    hdulist.close()
    for fits_file in fits_file_list[1:]:
        new_fits_file = fits_file
        hdulist       = fits.open(new_fits_file)
        new_exptime   = float(hdulist[0].header['EXPTIME'])
        new_unixtime  = float(hdulist[0].header['UNIXTIME'])
        hdulist.close()
        if new_exptime == old_exptime:
            exptime = old_exptime
            if new_unixtime - old_unixtime != exptime:
                flag_no_timing_errors = False
                print
                print bcolors.BOLDRED + "TIMING ERROR: new_UNIXTIME - old_UNIXTIME != EXPTIME" \
                      + bcolors.DEFAULT
                print "new_UNIXTIME - old_UNIXTIME =", new_unixtime - old_unixtime
                print "EXPTIME =", exptime
                print "old_fits_file =", old_fits_file
                print "old_UNIXTIME =", old_unixtime
                print "new_fits_file =", new_fits_file
                print "new_UNIXTIME =", new_unixtime
            # TODO: Add error checking for UTC, DATE-OBS using datetime module
            # print hdulist[0].header['UTC']
            # print hdulist[0].header['DATE-OBS']
        else:
            flag_no_timing_errors = False
            print
            print bcolors.BOLDRED + "TIMING ERROR: new_EXPTIME != old_EXPTIME" \
                  + bcolors.DEFAULT
            print "old_fits_file =", old_fits_file
            print "EXPTIME =", old_exptime
            print "new_fits_file =", new_fits_file
            print "EXPTIME =", new_exptime
        old_fits_file = new_fits_file
        old_exptime   = new_exptime
        old_unixtime  = new_unixtime

    print
    if flag_no_timing_errors:
        print bcolors.BOLDGREEN + "No timing errors were found." + bcolors.DEFAULT
    else:
        print bcolors.BOLDRED + "WARNING: Timing errors were found." + bcolors.DEFAULT
    print "End checking timestamps."
    print datetime.datetime.utcnow().isoformat()

if __name__ == "__main__":
    try:
        main()
    except:
        print
        print "Program stopped."
