#! /usr/bin/env python
"""
check_fits_timestamps.py

TODO: Format documentation following http://docs.python.org/devguide/documenting.html
"""

import sys
from astropy.io import fits

def main():
    """Main code.

    Modularize code to prevent code execution when being imported.

    """
    try:
        check_fits_timestamps()
    except:
        print "ERROR: check_fits_timestamps() failed."
        
    # try to execute check_fits_timestamps
    # report to stdout and append to log
    # wait 60 seconds
    # repeat
    # stop when killed

def check_fits_timestamps():
    """Check timestamps of FITS files.

    [SUMMARY]

    Args:
    [LIST ARGS]

    Returns:
    [LIST RETURNS]

    Raises:
    [LIST ERRORs]
    """

    # FITS files from Argos do not conform to FITS standard:
    # - Actual file length is smaller than expected standard.
    # - Illegal keyword 'NTP:GPS'
    fits_file_list = sys.argv[1:]
    for fits_file in fits_file_list:
        hdulist = fits.open(fits_file)
        unixtime = hdulist[0].header['UNIXTIME']
        print unixtime
        hdulist.close()
    
    # read list of file paths with timestamps to dict, key:value, filepath:timestamp
    # np arrays: [1:] - [0:-1]
    # where != exptime, find corresponding index from dict
    # export results of each check to a log

if __name__ == "__main__":
    main()
