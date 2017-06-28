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
m_command_args = utils.multicommand_arguments
STILTS = constants.STILTS


# =============================================================================
# Define functions
# =============================================================================
def addcol(name, expression, before=None, after=None, units=None, ucd=None,
           desc=None, infile=None, outfile=None):
    """
    Add a new column called "name" defined by the algebraic expression 
    "expression". 
    
    :param name: string, the new column name
    :param expression: string, the algebraic expression
    :param before: string, the column name to position the new column before
    :param after: string, the column name to position the new column after
    :param units: string, the units for the column
    :param ucd: string, the UCD for the column
    :param desc: string, the description for the column
    :param infile: string, the location and file name for the input file, if
                   not defined will return the STILTS command string
    :param outfile: string, the location and file name for the output file,
                    if not defined will default to infile
                   
    By default the new column appears after the last column of the table, 
    but you can position it either before or after a specified column using 
    the "before" or "after" flags respectively. 
    
    The "units", "ucd" and "desc" flags can be used to define 
    metadata values for the new column.

    equivalent STILTS command:
    
    addcol [-after <col-id> | -before <col-id>]
          [-units <units>] [-ucd <ucd>] [-utype <utype>] [-desc <descrip>]
          <col-name> <expr>
    
    :return: 
    """
    cmdstr = ""
    if before is not None:
        cmdstr += '-before {0}'.format(__checkq__(str(before)))
    if after is not None:
        cmdstr += '-after {0}'.format(__checkq__(str(after)))
    if units is not None:
        cmdstr += '-units {0} '.format(__checkq__(str(units)))
    if ucd is not None:
        cmdstr += '-ucd {0} '.format(__checkq__(str(ucd)))
    if desc is not None:
        cmdstr += '-desc {0} '.format(__checkq__(str(desc)))

    args = [cmdstr, name, __checkq__(expression)]
    if infile is None:
        return 'addcol {0} {1} {2}'.format(*args)
    if outfile is not None:
        cmdstr = 'addcol {0} {1} {2}'.format(*args)
        tpipe(cmds=cmdstr, infile=infile, outfile=outfile)
    else:
        cmdstr = 'addcol {0} {1} {2}'.format(*args)
        tpipe(cmds=cmdstr, infile=infile, outfile=infile)


def addcols(infile, names, expressions, befores=None, afters=None, units=None,
            ucds=None, descs=None, outfile=None):
    """
    Add new columns from list of "names" defined by the algebraic expressions 
    "expressions". 

    :param names: list of strings, the new column name for each column
    :param expressions: list of strings, the algebraic expression of each 
                        column
    :param befores: list of strings, the column name to position each new 
                    column before
    :param afters: list of strings, the column name to position each new 
                   column after
    :param units: list of strings, the units for each column
    :param ucds: list of strings, the UCD for each column
    :param descs: list of strings, the description for the column
    :param infile: string, the location and file name for the input file, if
                   not defined will return the STILTS command string
    :param outfile: string, the location and file name for the output file,
                    if not defined will default to infile

    By default the new columns appear after the last column of the table, 
    but you can position it either before or after a specified column using 
    the "befores" or "afters" flags respectively. 

    The "units", "ucds" and "descs" flags can be used to define 
    metadata values for the new column.

    this is equivalent to a for loop over the STILTS command:

    addcol [-after <col-id> | -before <col-id>]
          [-units <units>] [-ucd <ucd>] [-utype <utype>] [-desc <descrip>]
          <col-name> <expr>

    :return: 
    """
    ustr = ''
    for c in range(len(names)):
        kwargs = dict(infile=infile, outfile=outfile)
        kwargs = m_command_args('before', kwargs, befores, c)
        kwargs = m_command_args('after', kwargs, afters, c)
        kwargs = m_command_args('units', kwargs, units, c)
        kwargs = m_command_args('ucd', kwargs, ucds, c)
        kwargs = m_command_args('desc', kwargs, descs, c)
        ustr += addcol(names[c], expressions[c], **kwargs)

    if outfile is None:
        tpipe(cmds=ustr, infile=infile, outfile=outfile)
    else:
        tpipe(cmds=ustr, infile=infile, outfile=infile)


def addresolve(colid, racol, deccol, infile=None, outfile=None):
    """
    Performs name resolution on the "colid" and appends two new columns 
    "racol" and "deccol" containing the resolved Right Ascension and 
    Declination in degrees. 
    
    :param colid: string, column name to resolve against (online)
    :param racol: string, name of the new RA column
    :param deccol: string, name of the new Dec column
    :param infile: string, the location and file name for the input file, if
                   not defined will return the STILTS command string
    :param outfile: string, the location and file name for the output file,
                    if not defined will default to infile
                    
    UCDs are added to the new columns in a way which tries to be consistent 
    with any UCDs already existing in the table.

    Since this filter works by interrogating a remote service, it will 
    obviously be slow. The current implementation is experimental; it may 
    be replaced in a future release by some way of doing the same thing 
    (perhaps a new STILTS task) which is able to work more efficiently by 
    dispatching multiple concurrent requests.

    This is currently implemented using the Simbad service operated by CDS. 
    
    equivalent STILTS command:
    
    addresolve <col-id-objname> <col-name-ra> <col-name-dec>
    
    :return: 
    """
    args = [colid, racol, deccol]
    if infile is None:
        return 'addresolve {0} {1} {2}'.format(*args)
    if outfile is not None:
        cmdstr = 'addresolve {0} {1} {2}'.format(*args)
        tpipe(cmds=cmdstr, infile=infile, outfile=outfile)
    else:
        cmdstr = 'addresolve {0} {1} {2}'.format(*args)
        tpipe(cmds=cmdstr, infile=infile, outfile=infile)


def addskycoords(insys, outsys, incol1, incol2, outcol1=None, outcol2=None,
                 epoch=None, inunit=None, outunit=None, infile=None,
                 outfile=None):
    """
    Add new columns to the table representing position on the sky. 
    The values are determined by converting a sky position whose coordinates 
    are contained in existing columns. 

    :param insys: string, input coordinate system specifiers, must be one of
                  the following: 

                    - icrs: ICRS (Hipparcos) (Right Ascension, Declination)
                    - fk5: FK5 J2000.0 (Right Ascension, Declination)
                    - fk4: FK4 B1950.0 (Right Ascension, Declination)
                    - galactic: IAU 1958 Galactic (Longitude, Latitude)
                    - supergalactic: de Vaucouleurs Supergalactic 
                                     (Longitude, Latitude)
                    - ecliptic: Ecliptic (Longitude, Latitude)

    :param outsys: string, output coordinate system specifiers, must be one of
                  the following: 

                    - icrs: ICRS (Hipparcos) (Right Ascension, Declination)
                    - fk5: FK5 J2000.0 (Right Ascension, Declination)
                    - fk4: FK4 B1950.0 (Right Ascension, Declination)
                    - galactic: IAU 1958 Galactic (Longitude, Latitude)
                    - supergalactic: de Vaucouleurs Supergalactic 
                                     (Longitude, Latitude)
                    - ecliptic: Ecliptic (Longitude, Latitude)

    :param incol1: string, name of the input coordinate 1 column (e.g. RA)

    :param incol2: string, name of the input coordinate 2 column (e.g. Dec)

    :param outcol1: string, name of the output coordinate 1 column

    :param outcol2: string, name of the output coordinate 2 column

    :param epoch: float, epoch flag (used for certain conversions) default 
                  is 2000.0

    :param inunit: string, indicate the unit of the input coordinates, must be
                   one of the following:

                   - deg: for degrees
                   - rad: for radians
                   - sex: for sexagesimal

    :param outunit: string, indicate the unit of the output coordinates, must be
                    one of the following:

                   - deg: for degrees
                   - rad: for radians
                   - sex: for sexagesimal
                   
    :param infile: string, the location and file name for the input file, if
                   not defined will return the STILTS command string
                   
    :param outfile: string, the location and file name for the output file,
                    if not defined will default to infile
              
    Add new columns to the table representing position on the sky. 
    The values are determined by converting a sky position whose coordinates 
    are contained in existing columns. The "incol1" and "incol2" arguments 
    give identifiers for the two input coordinate columns in the 
    coordinate system named by "insys", and the "outcol1" and "outcol2" 
    arguments name the two new columns, which will be in the coordinate system 
    named by "outsys".
      
    equivalent STILTS command:
    
       addskycoords [-epoch <expr>] [-inunit deg|rad|sex] [-outunit deg|rad|sex]
                    <insys> <outsys> <col-id1> <col-id2> <col-name1> <col-name2>
                    
    :return: 
    """
    cmdstr = ""
    if outcol1 is None:
        outcol1 = incol1
    if outcol2 is None:
        outcol2 = incol2

    cunits = ['deg', 'degrees', 'rad', 'radians', 'sex', 'sexagesimal']
    if epoch is not None:
        try:
            cmdstr += '-epoch {0}'.format(float(epoch))
        except ValueError:
            raise ValueError('Error: epoch must be a float')
    if inunit is not None:
        if inunit not in cunits:
            raise ValueError('Error: inunit must be deg|rad|sex')
        cmdstr += '-inunit {0}'.format(inunit)
    if outunit is not None:
        if outunit not in cunits:
            raise ValueError('Error: outunit must be deg|rad|sex')
        cmdstr += '-outunit {0}'.format(outunit)

    args = [cmdstr, insys, outsys, incol1, incol2, outcol1, outcol2]
    if infile is None:
        return 'addskycoords {0} {1} {2} {3} {4} {5} {6}'.format(*args)
    if outfile is not None:
        ustr = 'addskycoords {0} {1} {2} {3} {4} {5} {6}'.format(*args)
        tpipe(cmds=ustr, infile=infile, outfile=outfile)
    else:
        ustr = 'addskycoords {0} {1} {2} {3} {4} {5} {6}'.format(*args)
        tpipe(cmds=ustr, infile=infile, outfile=infile)


def assert_(expression, infile=None, outfile=None):
    """
    Check that a boolean expression is true for each row. 
    
    If the "expression" does not evaluate true for any row of the table, 
    execution terminates with an error. As long as no error occurs, the output 
    table is identical to the input one. 
    
    :param expression: string, the algebraic expression that must evaluate to
                       True for at least one of the rows of the table
    
    :param infile: string, the location and file name for the input file, if
                   not defined will return the STILTS command string
                   
    :param outfile: string, the location and file name for the output file,
                    if not defined will default to infile
    :return: 
    """
    args = [expression]
    if infile is None:
        return 'assert {0}'.format(*args)
    if outfile is not None:
        cmdstr = 'assert {0}'.format(*args)
        tpipe(cmds=cmdstr, infile=infile, outfile=outfile)
    else:
        cmdstr = 'assert {0}'.format(*args)
        tpipe(cmds=cmdstr, infile=infile, outfile=infile)


def badval(badvalue, colname, infile=None, outfile=None):
    """
    For each column specified in "colname" any occurrence of the value 
    "badvalue" is replaced by a blank entry. 
    
    :param badvalue: string, value to replace
    
    :param colname: string, colname to search and replace bad values
    
    :param infile: string, the location and file name for the input file, if
                   not defined will return the STILTS command string
                   
    :param outfile: string, the location and file name for the output file,
                    if not defined will default to infile
    :return: 
    """
    args = [__checkq__(badvalue), __checkq__(colname)]
    if infile is None:
        return 'badval {0} {1}'.format(*args)
    if outfile is not None:
        cmdstr = 'badval {0} {1}'.format(*args)
        tpipe(cmds=cmdstr, infile=infile, outfile=outfile)
    else:
        cmdstr = 'badval {0} {1}'.format(*args)
        tpipe(cmds=cmdstr, infile=infile, outfile=infile)


def cache(infile=None, outfile=None):
    """
    Stores in memory or on disk a temporary copy of the table at this point in 
    the pipeline. This can provide improvements in efficiency if there is an 
    expensive step upstream and a step which requires more than one read of the 
    data downstream. If you see an error like "Can't re-read data from stream" 
    then adding this step near the start of the filters might help. 
    
    :param infile: string, the location and file name for the input file, if
                   not defined will return the STILTS command string
                   
    :param outfile: string, the location and file name for the output file,
                    if not defined will default to infile
    :return: 
    """
    if infile is None:
        return 'cache'
    if outfile is not None:
        cmdstr = 'cache'
        tpipe(cmds=cmdstr, infile=infile, outfile=outfile)
    else:
        cmdstr = 'cache'
        tpipe(cmds=cmdstr, infile=infile, outfile=infile)


def check(infile=None, outfile=None):
    """
    Runs checks on the table at the indicated point in the processing pipeline. 
    This is strictly a debugging measure, and may be time-consuming for 
    large tables.  

    :param infile: string, the location and file name for the input file, if
                   not defined will return the STILTS command string

    :param outfile: string, the location and file name for the output file,
                    if not defined will default to infile
    :return: 
    """
    if infile is None:
        return 'check'
    if outfile is not None:
        cmdstr = 'check'
        tpipe(cmds=cmdstr, infile=infile, outfile=outfile)
    else:
        cmdstr = 'check'
        tpipe(cmds=cmdstr, infile=infile, outfile=infile)


# TODO: clearparams FUNCTION
def clearparams(*pnames):
    """
    Currently not implemented 
    :param pnames:
    :return: 
    """
    raise NotImplementedError("clearparams function is not currently "
                              "implemented")


def colmeta(colname, infile=None, name=None, units=None, ucd=None, desc=None,
            outfile=None):
    """
    Modifies the metadata of one or more columns. Some or all of the name, 
    units, ucd, utype and description of the column(s), 
    identified by "colname" can be set by using some or all of the listed flags. 
    
    Typically, "colname" will simply be the name of a single column. 
    
    :param colname: string, name of the column to change meta data for
    
    :param infile: string, the location and file name for the input file, if
                   not defined will return the STILTS command string
                   
    :param outfile: string, the location and file name for the output file,
                    if not defined will default to infile
                    
    :param name: string, new name for the column
    
    :param units: string, new unit for the column
    
    :param ucd: string, new UCD for the column
    
    :param desc: string, new description for the column
    
    :return: 
    """
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
    if outfile is not None:
        tpipe(cmdstr, infile=infile, outfile=outfile)
    else:
        tpipe(cmdstr, infile=infile, outfile=infile)


def delcol(name, infile=None):
    """
    Delete the specified columns. The same column may harmlessly be specified 
    more than once. 
    
    :param name: string, the name of the column(s) to delete
    :param infile: string, the location and file name for the input file, if
                   not defined will return the STILTS command string
    :return: 
    """
    if infile is None:
        return delcols(name)
    else:
        delcols(name, infile=infile)


def delcols(names, infile=None):
    """
    Delete the specified columns. The same column may harmlessly be specified 
    more than once. 

    :param name: string, the name of the column(s) to delete
    :param infile: string, the location and file name for the input file, if
                   not defined will return the STILTS command string
    :return: 
    """
    if infile is None:
        return 'delcols {0}'.format(__checkq__(" ".join(names)))
    else:
        cmdstr = 'delcols {0}'.format(__checkq__(" ".join(names)))
        tpipe(cmds=cmdstr, infile=infile, outfile=infile)


def every(step, infile=None, outfile=None):
    """
    Include only every "step"th row in the result, starting with the first row. 
    
    :param step: int or string, starting with the first row only include every 
                 "step"th row
    
    :param infile: string, the location and file name for the input file, if
                   not defined will return the STILTS command string
                   
    :param outfile: string, the location and file name for the output file,
                    if not defined will default to infile
    :return: 
    """
    try:
        step = int(step)
    except ValueError:
        raise ValueError("Error: step must be an integer number")
    if infile is None:
        return 'step {0}'.format(step)
    if outfile is not None:
        cmdstr = 'step {0}'.format(step)
        tpipe(cmds=cmdstr, infile=infile, outfile=outfile)
    else:
        cmdstr = 'step {0}'.format(step)
        tpipe(cmds=cmdstr, infile=infile, outfile=infile)


# TODO: explodeall FUNCTION
def explodeall(ifndim, ifshape):
    """
    Currently not implemented
    :param ifndim:
    :param ifshape:
    :return: 
    """
    raise NotImplementedError("explodeall function is not currently "
                              "implemented")


# TODO: explodecols FUNCTION
def explodecols(colnames):
    """
    Currently not implemented
    :param colnames: 
    :return: 
    """
    raise NotImplementedError("explodecols function is not currently "
                              "implemented")


def fixcolnames(infile=None, outfile=None):
    """
    Renames all columns and parameters in the input table so that they have 
    names which have convenient syntax for STILTS. For the most part this 
    means replacing spaces and other non-alphanumeric characters with 
    underscores. 
    
    This is a convenience which lets you use column names in algebraic 
    expressions and other STILTS syntax. 

    :param infile: string, the location and file name for the input file, if
                   not defined will return the STILTS command string

    :param outfile: string, the location and file name for the output file,
                    if not defined will default to infile
    :return: 
    """
    if infile is None:
        return 'fixcolnames'
    if outfile is not None:
        cmdstr = 'fitcolnames'
        tpipe(cmds=cmdstr, infile=infile, outfile=outfile)
    else:
        cmdstr = 'fitcolnames'
        tpipe(cmds=cmdstr, infile=infile, outfile=infile)


def head(nrows, infile=None, outfile=None):
    """
    Include only the first "nrows" rows of the table. If the table has fewer 
    than "nrows" rows then it will be unchanged. 
    
    :param nrows: int, the number of rows (from the first row) to keep
    
    :param infile: string, the location and file name for the input file, if
                   not defined will return the STILTS command string

    :param outfile: string, the location and file name for the output file,
                    if not defined will default to infile
    :return: 
    """
    try:
        nrows = int(nrows)
    except ValueError:
        raise ValueError('Error: nrows must be an integer')
    if infile is None:
        return 'head {0}'.format(nrows)
    if outfile is not None:
        cmdstr = 'head {0}'.format(nrows)
        tpipe(cmds=cmdstr, infile=infile, outfile=outfile)
    else:
        cmdstr = 'head {0}'.format(nrows)
        tpipe(cmds=cmdstr, infile=infile, outfile=infile)


def keepcols(names, infile=None):
    if infile is None:
        return 'keepcols {0}'.format(__checkq__(" ".join(names)))
    else:
        cmdstr = 'keepcols {0}'.format(__checkq__(" ".join(names)))
        tpipe(cmds=cmdstr, infile=infile, outfile=infile)


# TODO: meta FUNCTION
def meta(*items):
    """
    Currently not implemented 
    :param items:
    :return: 
    """
    raise NotImplementedError("meta function is not currently implemented")


def progress(infile=None, outfile=None):
    """
    Monitors progress by displaying the number of rows processed so far on the 
    terminal (standard error). This number is updated every second or 
    thereabouts; if all the processing is done in under a second you may not 
    see any output. If the total number of rows in the table is known, an 
    ASCII-art progress bar is updated, otherwise just the number of rows seen 
    so far is written.

    Note under some circumstances progress may appear to complete before the 
    actual work of the task is done since part of the processing involves 
    slurping up the whole table to provide random access on it. In this case, 
    applying the cache upstream may help. 

    :param infile: string, the location and file name for the input file, if
                   not defined will return the STILTS command string

    :param outfile: string, the location and file name for the output file,
                    if not defined will default to infile
    :return: 
    """
    if infile is None:
        return 'progress'
    if outfile is not None:
        cmdstr = 'progress'
        tpipe(cmds=cmdstr, infile=infile, outfile=outfile)
    else:
        cmdstr = 'progress'
        tpipe(cmds=cmdstr, infile=infile, outfile=infile)


def random(infile=None, outfile=None):
    """
    Ensures that random access is available on this table. If the table 
    currently has random access, it has no effect. If only sequential access 
    is available, the table is cached so that downstream steps will see the 
    cached, hence random-access, copy. 

    :param infile: string, the location and file name for the input file, if
                   not defined will return the STILTS command string

    :param outfile: string, the location and file name for the output file,
                    if not defined will default to infile
    :return: 
    """
    if infile is None:
        return 'random'
    if outfile is not None:
        cmdstr = 'random'
        tpipe(cmds=cmdstr, infile=infile, outfile=outfile)
    else:
        cmdstr = 'random'
        tpipe(cmds=cmdstr, infile=infile, outfile=infile)


def randomview(infile=None, outfile=None):
    """
    Ensures that steps downstream only use random access methods for table 
    access. If the table is sequential only, this will result in an error. 
    Only useful for debugging.

    :param infile: string, the location and file name for the input file, if
                   not defined will return the STILTS command string

    :param outfile: string, the location and file name for the output file,
                    if not defined will default to infile
    :return: 
    """
    if infile is None:
        return 'randomview'
    if outfile is not None:
        cmdstr = 'randomview'
        tpipe(cmds=cmdstr, infile=infile, outfile=outfile)
    else:
        cmdstr = 'randomview'
        tpipe(cmds=cmdstr, infile=infile, outfile=infile)


def renamecol(oldname, newname, infile=None, outfile=None):
    """
    Rename column "oldname" to "newname"

    :param oldname: string, old column name
    
    :param newname: string, new column name
    
    :param infile: string, the location and file name for the input file, if
                   not defined will return the STILTS command string

    :param outfile: string, the location and file name for the output file,
                    if not defined will default to infile
    :return: 
    """
    ustr = updatemetadata(oldname, name=newname)
    if infile is None:
        return ustr
    if outfile is not None:
        tpipe(cmds=ustr, infile=infile, outfile=outfile)
    else:
        tpipe(cmds=ustr, infile=infile, outfile=infile)


def renamecols(oldnames, newnames, infile=None, outfile=None):
    """
    Rename column "oldname" to "newname"

    :param oldnames: list of strings, old column names

    :param newnames: list of strings, new column names

    :param infile: string, the location and file name for the input file, if
                   not defined will return the STILTS command string

    :param outfile: string, the location and file name for the output file,
                    if not defined will default to infile
    :return: 
    """
    ustrs = ""
    for c in range(len(oldnames)):
        ustr = updatemetadata(oldnames[c], name=newnames[c])
        tpipe(cmds=ustr, infile=infile, outfile=infile)
        if infile is None:
            ustrs += "{0} ".format(ustr)
        if outfile is not None:
            tpipe(cmds=ustr, infile=infile, outfile=outfile)
        else:
            tpipe(cmds=ustr, infile=infile, outfile=infile)
    if infile is None:
        return ustrs


# TODO: repeat FUNCTION
def repeat(count, row=None, table=None):
    """
    Currently not implemented 
    :param count:
    :param row:
    :param table:
    :return: 
    """
    raise NotImplementedError("repeat function is not currently "
                              "implemented")


def replacecol(colname, expression, infile=None):
    if infile is None:
        return 'replacecol {0} {1} '.format(colname, __checkq__(expression))
    else:
        cmdstr = 'replacecol {0} {1} '.format(colname, __checkq__(expression))
        tpipe(cmd=cmdstr, infile=infile, outfile=infile)


def replacecols(infile, names, expressions):
    ustr = ''
    for c in range(len(names)):
        ustr += replacecol(names[c], expressions[c], infile=None)
    tpipe(cmds=ustr, infile=infile, outfile=infile)


# TODO: replaceval FUNCTION
def replaceval(colname, old, new):
    """
    Currently not implemented 
    :param colname:
    :param old:
    :param new:
    :return: 
    """
    raise NotImplementedError("replaceval function is not currently "
                              "implemented")


# TODO: rowrange FUNCTION
def rowrange(first, last=None, count=None):
    """
    Currently not implemented 
    :param first:
    :param last:
    :param count:
    :return: 
    """
    raise NotImplementedError("rowrange function is not currently "
                              "implemented")


# TODO: select FUNCTION
def select(expression):
    """
    Currently not implemented 
    :param expression:
    :return: 
    """
    raise NotImplementedError("select function is not currently "
                              "implemented")


# TODO: seqview FUNCTION
def seqview():
    """
    Currently not implemented 
    :return: 
    """
    raise NotImplementedError("seqview function is not currently "
                              "implemented")


# TODO: setparam FUNCTION
def setparam():
    """
    Currently not implemented 
    :return: 
    """
    raise NotImplementedError("setparam function is not currently "
                              "implemented")


# TODO: sort FUNCTION
def sort():
    """
    Currently not implemented 
    :return: 
    """
    raise NotImplementedError("sort function is not currently implemented")


# TODO: sorthead FUNCTION
def sorthead():
    """
    Currently not implemented 
    :return: 
    """
    raise NotImplementedError("sorthead function is not currently implemented")


# TODO: stats FUNCTION
def stats(*items):
    """
    Currently not implemented 
    :param items:
    :return: 
    """
    raise NotImplementedError("stats function is not currently implemented")


# TODO: tablename FUNCTION
def tablename(name):
    """
    Currently not implemented 
    :param name:
    :return: 
    """
    raise NotImplementedError("tablename function is not currently implemented")


# TODO: tail FUNCTION
def tail(nrows):
    """
    Currently not implemented 
    :param nrows:
    :return: 
    """
    raise NotImplementedError("tail function is not currently implemented")


# TODO: transpose FUNCTION
def transpose(colname, columnnames=None):
    """
    Currently not implemented 
    :param colname:
    :param columnnames:
    :return: 
    """
    raise NotImplementedError("transpose function is not currently implemented")


# TODO: uniq FUNCTION
def uniq(colname, count=None):
    """
    Currently not implemented 
    :param colname:
    :param count:
    :return: 
    """
    raise NotImplementedError("uniq function is not currently implemented")


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
                   desc=None, outfile=None):
    """
    Modifies the metadata of one or more columns. Some or all of the name, 
    units, ucd, utype and description of the column(s), 
    identified by "colname" can be set by using some or all of the listed flags. 

    Typically, "colname" will simply be the name of a single column. 

    :param colname: string, name of the column to change meta data for

    :param infile: string, the location and file name for the input file, if
                   not defined will return the STILTS command string

    :param outfile: string, the location and file name for the output file,
                    if not defined will default to infile

    :param name: string, new name for the column

    :param units: string, new unit for the column

    :param ucd: string, new UCD for the column

    :param desc: string, new description for the column

    :return: 
    """
    if infile is None:
        return colmeta(colname, infile, name, units, ucd, desc, outfile)
    else:
        colmeta(colname, infile, name, units, ucd, desc, outfile)

