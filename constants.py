#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 02/06/17 at 2:26 PM

@author: neil

Program description here

Version 0.0.0
"""
from astropy import units as u
import numpy as np
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(),
                                             os.path.dirname(__file__)))

# =============================================================================
# Define functions
# =============================================================================
def read_config_file():
    if 'config.txt' not in os.listdir(__location__):
        raise FileNotFoundError("Config file missing...")
    # Load config file

    keys, values = np.loadtxt(__location__ + '/config.txt', dtype=bytes,
                              delimiter='=', unpack=True).astype(str)
    filedict = dict(zip(keys, values))
    # strip white spaces
    for key in list(filedict.keys()):
        filedict[key.strip()] = filedict[key].strip()
    # Set up default values
    data = dict()
    data['STILTS_CMD'] = ['java -jar topcat-full.jar -stilts']
    # Update the values from file if found
    for r, rkey in enumerate(list(data.keys())):
        if rkey in list(filedict.keys()):
            data[rkey] = filedict[rkey]
    # return config dictionary
    return data


# =============================================================================
# Define variables
# =============================================================================
CONFIG = read_config_file()
UUNIT = u.core.Unit
UQUANT = u.quantity.Quantity
STILTS = CONFIG['STILTS_CMD']
