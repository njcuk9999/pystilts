#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 02/06/17 at 2:26 PM

@author: neil

Program description here

Version 0.0.0
"""
from astropy import units as u
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(),
                                             os.path.dirname(__file__)))

# =============================================================================
# Define functions
# =============================================================================
def _default_data_dir():
    xdg_data_home = os.environ.get('XDG_DATA_HOME')
    if xdg_data_home:
        return os.path.join(xdg_data_home, 'pystilts')
    return os.path.join(os.path.expanduser('~'), '.local', 'share', 'pystilts')


def _parse_config_file(config_path):
    data = {}
    if not os.path.exists(config_path):
        return data
    with open(config_path, 'r', encoding='utf-8') as fobj:
        for line in fobj:
            stripped = line.strip()
            if not stripped or stripped.startswith('#') or '=' not in stripped:
                continue
            key, value = stripped.split('=', 1)
            data[key.strip()] = value.strip()
    return data


def read_config_file():
    config_path = os.path.join(__location__, 'config.txt')
    filedict = _parse_config_file(config_path)

    data = {
        'STILTS_CMD': 'java -jar topcat-full.jar -stilts',
    }

    for key in list(data.keys()):
        if key in filedict:
            data[key] = filedict[key]

    env_stilts = os.environ.get('PYSTILTS_STILTS_CMD')
    if env_stilts:
        data['STILTS_CMD'] = env_stilts

    if 'STILTS_CMD' not in filedict and not env_stilts:
        bundled_jar = os.path.join(_default_data_dir(), 'topcat-full.jar')
        if os.path.exists(bundled_jar):
            data['STILTS_CMD'] = 'java -jar {0} -stilts'.format(bundled_jar)

    return data


# =============================================================================
# Define variables
# =============================================================================
CONFIG = read_config_file()
UUNIT = u.core.Unit
UQUANT = u.quantity.Quantity
STILTS = CONFIG['STILTS_CMD']
