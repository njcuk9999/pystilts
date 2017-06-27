#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 02/06/17 at 2:28 PM

@author: neil

Program description here

Version 0.0.0
"""
from . import constants

import subprocess as sb
import os
import xml.etree.ElementTree as ET


# =============================================================================
# Define variables
# =============================================================================
UUNIT = constants.UUNIT
UQUANT = constants.UQUANT


# =============================================================================
# Command functions
# =============================================================================
def runcommand(command, print_input=False, print_output=False, print_err=True,
               return_result=False):
    res = sb.Popen(command, stdout=sb.PIPE, stderr=sb.PIPE,
                     universal_newlines=True, shell=True)
    res.wait()
    result = res.communicate()
    if print_input:
        print(command)
    if print_output:
        print(result[0])
    if result[1] != '' and print_err:
        print(result[1])
    if return_result:
        return result


def command_arguments(keys, kwargs, callname):
    commanddict = dict()
    # set the default values
    for key in list(keys.keys()):
        params = keys[key]
        # if we have a default value set it
        if 'd' in params:
            # deal with units
            if type(params['d']) in [UUNIT, UQUANT]:
                # if we have default units assigned
                if 'u' in params:
                    value = (params['d']).to(params['u']).value
                else:
                    value = params['d'].value
            else:
                value = params['d']
            commanddict[key] = '{0}=\'{1}\' '.format(key, value)
        # if required
        required = params.get('r', False)
        if required:
            has_kwarg = False
            for kwarg in list(kwargs.keys()):
                if kwarg in params['v']:
                    has_kwarg = True
            if not has_kwarg:
                emsg = 'Value "{0}" is required by {1}'
                raise KeyError(emsg.format(key, callname))
        # finally set key from kwargs
        for kwarg in list(kwargs.keys()):
            for vkey in params['v']:
                if kwarg == vkey:
                    # deal with units
                    if type(kwargs[kwarg]) in [UUNIT, UQUANT]:
                        # if we have default units assigned
                        if 'u' in params:
                            value = (kwargs[vkey]).to(params['u']).value
                        else:
                            value = kwargs[vkey].value
                    else:
                        value = kwargs[vkey]
                    commanddict[key] = '{0}=\'{1}\' '.format(key, value)
    # return
    return commanddict


def multicommand_arguments(key, kwargs, values, element):
    if values is not None:
        if type(values) != str and hasattr(values, '__len__'):
            kwargs[key] = values[element]
        else:
            kwargs[key] = values
    return kwargs


# =============================================================================
# File functions
# =============================================================================
def clean_file(datafile):
    tree = ET.parse(datafile)
    root = tree.getroot()
    remove_children = []
    children = []
    for c, child in enumerate(root[0][0]):
        if 'PARAM' in child.tag:
            remove_children.append(child)
        elif 'FIELD' in child.tag:
            root[0][0][c].attrib['ID'] = child.attrib['name']
            children.append(child)
        else:
            children.append(child)
    # remove PARAM children (if any)
    if len(remove_children) > 0:
        for child in root[0][0].findall(remove_children[0].tag):
            root[0][0].remove(child)
    # write to file
    tree.write(datafile)

    # for some reason this adds 'ns0:' to the parmeters so need to remove this
    f = open(datafile, 'r')
    lines = f.readlines()
    f.close()
    newlines = ['<?xml version=\'1.0\'?>\n']
    for l_it in range(len(lines)):
        newlines.append(lines[l_it].replace('ns0:', ''))
    os.remove(datafile)
    f = open(datafile, 'w')
    f.writelines(newlines)
    f.close()




