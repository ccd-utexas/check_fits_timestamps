#! /usr/bin/env python
"""check_fits_timestamps.py

Calls check_fits_timestamps module to compare timestamps between pairs of
subsequent FITS files to check that timestamps are separated by the
exposure time. This program is specific to Argos data.

Example use:
check_fits_timestamps.py /path/to/data/A1234.*.fits
Must call with 2 or more FITS files.
"""
# TODO: Format documentation following
# http://docs.python.org/devguide/documenting.html

import sys
from astropy.io import fits
import time
import datetime as dt

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
    while True:
        check_fits_timestamps()
        print
        print stop_instructions
        sleep_time = 60 # seconds
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
    2 or more FITS files.

    Returns:
    Prints to stdout.
    """
    # FITS files from Argos do not conform to FITS standard:
    # - Actual file length is smaller than expected standard.
    # - Illegal keyword 'NTP:GPS'
    fits_file_list = sys.argv[1:]

    print
    if len(fits_file_list) < 2:
        print "Must call with 2 or more FITS files."
        print "Example use:"
        print "check_fits_timestamps.py /path/to/data/A1234.*.fits"
        sys.exit()
    print dt.datetime.utcnow().isoformat()
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
    # TODO: Combine UTC and DATE-OBS. Just report strings for now.
    # old_utc        = dt.datetime.strptime(hdulist[0].header['UTC'], "%H:%M:%S")
    # old_dateobs    = dt.datetime.strptime(hdulist[0].header['DATE-OBS'], "%Y-%m-%d")
    old_utc        = hdulist[0].header['UTC']
    old_dateobs    = hdulist[0].header['DATE-OBS']
    hdulist.close()
    for fits_file in fits_file_list[1:]:
        new_fits_file = fits_file
        hdulist       = fits.open(new_fits_file)
        new_exptime   = float(hdulist[0].header['EXPTIME'])
        new_unixtime  = float(hdulist[0].header['UNIXTIME'])
        # TODO: Combine UTC and DATE-OBS. Just report strings for now
        # new_utc       = dt.datetime.strptime(hdulist[0].header['UTC'], "%H:%M:%S")
        # new_dateobs   = dt.datetime.strptime(hdulist[0].header['DATE-OBS'], "%Y-%m-%d")
        new_utc        = hdulist[0].header['UTC']
        new_dateobs    = hdulist[0].header['DATE-OBS']
        hdulist.close()
        # Check that EXPTIMEs of both files is same.
        if new_exptime == old_exptime:
            exptime = old_exptime
            # Compare Posix timestamps to EXPTIME test timing for now.
            # TODO: Use datetime.deltatime to compare UTC and DATE-OBS.
            if new_unixtime - old_unixtime != exptime:
                flag_no_timing_errors = False
                print
                print bcolors.BOLDRED + "TIMING ERROR: new_UNIXTIME - old_UNIXTIME != EXPTIME" \
                      + bcolors.DEFAULT
                print "new_UNIXTIME - old_UNIXTIME =", new_unixtime - old_unixtime
                print "EXPTIME =", exptime
                print "old_fits_file =", old_fits_file
                print "old_UNIXTIME  =", old_unixtime
                print "old_UTC       =", old_utc
                print "old_DATE-OBS  =", old_dateobs
                print "new_fits_file =", new_fits_file
                print "new_UNIXTIME  =", new_unixtime
                print "new_UTC       =", new_utc
                print "new_DATE-OBS  =", new_dateobs
        # Error if EXPTIMEs of two files is different.
        else:
            flag_no_timing_errors = False
            print
            print bcolors.BOLDRED + "TIMING ERROR: new_EXPTIME != old_EXPTIME" \
                  + bcolors.DEFAULT
            print "old_fits_file =", old_fits_file
            print "EXPTIME       =", old_exptime
            print "new_fits_file =", new_fits_file
            print "EXPTIME       =", new_exptime
        # Set current "new" values to "old" in prep for comparison with next file.
        old_fits_file = new_fits_file
        old_exptime   = new_exptime
        old_unixtime  = new_unixtime
        old_utc       = new_utc
        old_dateobs   = new_dateobs

    print
    if flag_no_timing_errors:
        print bcolors.BOLDGREEN + "No timing errors were found." + bcolors.DEFAULT
    else:
        print bcolors.BOLDRED + "WARNING: Timing errors were found." + bcolors.DEFAULT
    print "End checking timestamps."
    print dt.datetime.utcnow().isoformat()

if __name__ == "__main__":
    try:
        main()
    except:
        print
        print "Program stopped."
