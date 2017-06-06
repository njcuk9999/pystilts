#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 02/06/17 at 2:24 PM

@author: neil

Program description here

Version 0.0.0
"""
from . import constants
from . import utils

# =============================================================================
# Define variables
# =============================================================================
runcommand = utils.runcommand
command_arguments = utils.command_arguments
STILTS = constants.STILTS


# =============================================================================
# Define functions
# =============================================================================
def addcol(name, expression, infile=None):
    if infile is None:
        return 'addcol {0} {1} '.format(name, __checkq__(expression))
    else:
        cmdstr = 'addcol {0} {1}'.format(name, __checkq__(expression))
        tpipe(cmds=cmdstr, infile=infile, outfile=infile)


def addcols(infile, names, expressions):
    ustr = None
    for c in range(len(names)):
        ustr = addcol(names[c], expressions[c], infile=None)
    tpipe(cmds=ustr, infile=infile, outfile=infile)


def delcols(names, infile=None):
    if infile is None:
        return 'delcols {0}'.format(__checkq__(" ".join(names)))
    else:
        cmdstr = 'delcols {0}'.format(__checkq__(" ".join(names)))
        tpipe(cmds=cmdstr, infile=infile, outfile=infile)


def keepcols(names, infile=None):
    if infile is None:
        return 'keepcols {0}'.format(__checkq__(" ".join(names)))
    else:
        cmdstr = 'keepcols {0}'.format(__checkq__(" ".join(names)))
        tpipe(cmds=cmdstr, infile=infile, outfile=infile)


def renamecol(infile, oldname, newname):
    ustr = updatemetadata(oldname, name=newname)
    tpipe(cmds=ustr, infile=infile, outfile=infile)


def renamecols(infile, oldnames, newnames):
    ustr = None
    for c in range(len(oldnames)):
        ustr = updatemetadata(oldnames[c], name=newnames[c])
    tpipe(cmds=ustr, infile=infile, outfile=infile)


def replacecols(infile, names, expressions):
    ustr = None
    for c in range(len(names)):
        ustr = replacecol(names[c], expressions[c], infile=None)
    tpipe(cmds=ustr, infile=infile, outfile=infile)


def replacecol(colname, expression, infile=None):
    if infile is None:
        return 'replacecol {0} {1} '.format(colname, __checkq__(expression))
    else:
        cmdstr = 'replacecol {0} {1} '.format(colname, __checkq__(expression))
        tpipe(cmd=cmdstr, infile=infile, outfile=infile)


def __checkq__(expression):
    expression = expression.replace('"', '').replace("'", '')
    expression = '"{0}"'.format(expression)
    return expression


def tpipe(cmds=None, **kwargs):

    # cmds is a special case has no argument (just insert onto command line)
    if cmds is None:
        command = "{0} {1} ".format(STILTS, "tpipe")
    else:
        command = "{0} {1} cmd=\'{2}\' ".format(STILTS, "tpipe", cmds)
    # define allowed arguments (must be in allowed or special)
    # v = aliases for command call
    # r = will throw exception if not defined
    # d = sets default value (if r = False)
    keys = dict()
    keys["ifmt"] = dict(v=["ifmt"], r=False)
    keys["istream"] = dict(v=["istream"], r=False)
    keys["cmd"] = dict(v=["cmd"], r=False)
    keys["omode"] = dict(v=["omode"], r=False)
    keys["out"] = dict(v=["outfile", "out"], r=True)
    keys["ofmt"] = dict(v=["ofmt"], r=False)
    keys["in"] = dict(v=["infile", "in"], r=True)
    # write the command
    commandargs = command_arguments(keys, kwargs, "tmatch2")
    for key in commandargs:
        command += commandargs[key]

    runcommand(command)


def updatemetadata(colname, infile=None, name=None, units=None, ucd=None,
                   desc=None):
    cmdstr = "colmeta "
    if name is None and units is None and ucd is None and desc is None:
        return 0
    if name is not None:
        cmdstr += '-name {0} '.format(__checkq__(str(name)))
    if units is not None:
        cmdstr += '-units {0} '.format(__checkq__(str(units)))
    if ucd is not None:
        cmdstr += '-ucd {0} '.format(__checkq__(str(ucd)))
    if desc is not None:
        cmdstr += '-desc {0} '.format(__checkq__(str(desc)))

    cmdstr += '{0}'.format(colname)

    if infile is None:
        return cmdstr
    else:
        tpipe(cmdstr, infile=infile, outfile=infile)







