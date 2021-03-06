#!/usr/bin/python
# -*- coding: utf-8 -*-

# Python imports
# import sys
import argparse
import re

# import datetime

# Numpy imports
import numpy as np

first_ionisation_potential = [
        13.60, 24.59,  5.39,  9.32,  8.30, 11.26, 14.53, 13.62, 17.40,
        21.56,  5.14,  7.64,  5.99,  8.15, 10.48, 10.36, 12.97, 15.76,
        04.34,  6.11,  6.54,  6.82,  6.74,  6.77,  7.44,  7.87,  7.86,
        07.64,  7.73,  9.39,  6.00,  7.88,  9.81,  9.75, 11.81, 14.00,
        04.18,  5.69,  6.38,  6.84,  6.88,  7.10,  7.28,  7.36,  7.46,
        08.33,  7.57,  8.99,  5.79,  7.34,  8.64,  9.01, 10.45, 12.13,
        03.89,  5.21,  5.58,  5.65,  5.42,  5.49,  5.55,  5.63,  5.68,
        06.16,  5.85,  5.93,  6.02,  6.10,  6.18,  6.25,  5.43,  7.00,
        07.88,  7.98,  7.87,  8.50,  9.10,  9.00,  9.22, 10.44,  6.11,
        07.42,  7.29,  8.42,  9.30, 10.75,  4.00,  5.28,  6.90,  6.08,
        09.99,  6.00]
second_ionisation_potential = [
        00.00, 54.42, 75.64, 18.21, 25.15, 24.38, 29.60, 35.12, 35.00,
        40.96, 47.29, 15.03, 18.83, 16.35, 19.72, 23.33, 23.81, 27.62,
        31.63, 11.87, 12.80, 13.58, 14.65, 16.50, 15.64, 16.18, 17.06,
        18.17, 20.29, 17.96, 20.51, 15.93, 18.63, 21.19, 21.60, 24.36,
        27.50, 11.03, 12.24, 13.13, 14.32, 16.15, 15.26, 16.76, 18.07,
        19.42, 21.49, 16.90, 18.87, 14.63, 16.53, 18.60, 19.13, 21.21,
        25.10, 10.00, 11.06, 10.85, 10.55, 10.73, 10.90, 11.07, 11.25,
        12.10, 11.52, 11.67, 11.80, 11.93, 12.05, 12.17, 13.90, 14.90,
        16.20, 17.70, 16.60, 17.50, 20.00, 18.56, 20.50, 18.76, 20.43,
        15.03, 16.68, 19.00, 20.00, 21.00, 22.00, 10.14, 12.10, 11.50,
        99.99, 12.00]
periodic_table = [
        'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
        'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca',
        'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
        'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr',
        'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn',
        'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd',
        'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb',
        'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg',
        'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th',
        'Pa', 'U']
gamma = {
        '1': {
                'Ca': 1.4,
                'Sr': 1.8,
                'Ba': 3.0,
            },
        '2': {
                'Na': 2.0,
                'Si': 1.3,
                'Ca': 1.8,
                'Fe': 1.4,
            }
         }
from_roman = {
        'I':    '1',
        'II':   '2',
        'III':  '3',
        'IV':   '4',
        'V':    '5'
            }
to_roman = {
        '1':    'I',
        '2':    'II',
        '3':    'III',
        '4':    'IV',
        '5':    'V'
        }
# Some constant that are used to filter out lines
# Maximum ionisation state that will be considered
Max_ion = 2
# Maximum excitation potential of the lower level
ChiexLowerMax = 15


def vald2bsyn():
    # First, we read the VALD file.
    print('Reading input file : {valdfile}'.format(valdfile=arguments.valdfile))
    valddata = readvald(arguments.valdfile)
    identifiedlines = identify(valddata)
    writebsynfile(identifiedlines, arguments.bsynfile)


def writebsynfile(lines, bsynfile):
    print('Writing data to BSyn file : {bsynfile}'.format(bsynfile=bsynfile))
    atomicnumber = []
    for k in lines.keys():
        atomicnumber.append(list(lines[k].keys())[0])

    with open(bsynfile, 'w') as bfile:
        for k in lines.keys():
            subkeys = list(lines[k].keys())
            a, i = k.split(' ')
            if np.int(i) > Max_ion:
                continue
            for subkey in subkeys:
                # format for the subheader is : '20X' 5f 10f
                # The decimal dot of the ID should be at column 6, which means that there are 4 spaces left before, which allows for ID like 1212.019016, should we have Mg2
                dot = subkey.index('.')
                IDL, IDR = subkey.split('.')
                stringID = '{{0: >{0}}}'.format(6-dot+1).format(IDL)+'.'+'{0: <15}'.format(IDR)
                ii = '{{:>{0}}}'.format(5).format(i)
                nlines = len(lines[k][subkey])
                nlines = '{:>10}'.format(nlines)
                subheader = "'" + stringID + "'" + ii + nlines + '\n'
                bfile.write(subheader)
                try:
                    elt = a + ' ' + to_roman[i]
                    element = "'" + '{{0:<{0}}}'.format(7).format(elt) + "'" + '\n'
                    bfile.write(element)
                except KeyError:
                    print('no key')
                    continue
                for index in range(len(lines[k][subkey])):
                    # We now write the atomica data to the file
                    bfile.write(lines[k][subkey][index])
                    bfile.write('\n')


def readvald(valdfile):
    with open(valdfile, 'r') as f:
        linedata = []
        for line in f:
            # Let's filter first all lines in the file that are not line data. These lines do not start with a single quote
            if not line.startswith(("'")):
                continue
            # Everything else is part of the line list
            linedata.append(line)

    return linedata


def identify(data):
    # The information lies at the end of each fourth line.
    isotoperegex = re.compile('\(([0-9]+)\)([A-Za-z]+)(\(([0-9]+)\)([A-Za-z]+))?')
    result = {}
    eqw = '0.0'
    eqwerr = '1.0'
    for index in range(len(data)//4):
        # We read the lines four by four
        lineinfo = data[4*index:4*index+4]
        if '**'in lineinfo[0]:
            continue
        isotopes = None
        isotopes = isotoperegex.search(lineinfo[3])
        lowerorbital, upperorbital, comment = identify_levels(lineinfo[1:3])
        elements = None
        if isotopes:
            elements = isotopes.groups()
        # Now we get the elements involved. It's the first field before the comma in the first line.
        compound, wavelength, loggf, chiexlower, jlow, chiexupper, jup, lowerlevel, upperlevel, mean, gamrad, stark, vdw, *rest = lineinfo[0].split(',')
        wavelength = np.float(wavelength)
        atom = compound.split(' ')[0].replace("'", '')
        loggf = np.float(loggf)
        if loggf <= -10.0:
            loggf = "{0:.2f}".format(loggf)
        else:
            loggf = "{0:.3f}".format(loggf)
        chiexlower = np.float(chiexlower)
        jup = np.float(jup)
        vdw = np.float(vdw)
        gamrad = np.float(gamrad)
        chiexlower = np.float(chiexlower)
        chiexupper = np.float(chiexupper)
        compound = compound.replace("'", "")
        ID, ionisation_stage = build_identification(compound, elements)
        if atom in periodic_table:
            if ((chiexupper > first_ionisation_potential[periodic_table.index(atom)]) and (ionisation_stage == '1')) or (chiexupper > second_ionisation_potential[periodic_table.index(atom)]):
                continue
        if chiexlower >= ChiexLowerMax:
            # We skip lines with lower level chiex greater than 15 eV
            continue

        if vdw == 0:
            # Van der Waals damping not provided by VALD. We'll use default values.
            # The elements are either isotopes or compounds.
            # By default, vdw is 2.5
            vdw = 2.5
            atom = compound.split(' ')[0]
            if atom in periodic_table:
                # We only modify ionisation stage 1 and 2 and for a few atoms.
                try:
                    vdw = gamma[str(ionisation_stage)][str(atom)]
                except KeyError:
                    pass
        if gamrad > 3.0:
            gamrad = 10**gamrad
        else:
            gamrad = 10**5
        wavelength = "{0:.3f}".format(wavelength)
        wavelength = '{0:>10}'.format(wavelength)
        chiexlower = "{0:.3f}".format(chiexlower)
        chiexlower = '{:>7}'.format(chiexlower)
        loggf = str(loggf)
        loggf = '{:>7}'.format(loggf.replace(' ', ''))
        vdw = "{0:.3f}".format(vdw)
        vdw = '{:>9}'.format(vdw)
        jup = "{0:.1f}".format(2*jup+1)
        jup = '{:>7}'.format(jup)
        gamrad = "{0:.2E}".format(gamrad)
        gamrad = '{:>10}'.format(gamrad)
        lowerorbital = "'" + str(lowerorbital) + "'"
        lowerorbital = '{:>4}'.format(lowerorbital)
        upperorbital = "'" + str(upperorbital) + "'"
        upperorbital = '{:>4}'.format(upperorbital)
        eqw = '{:>6}'.format(eqw.replace(' ', ''))
        eqwerr = '{:>7}'.format(eqwerr.replace(' ', ''))

        datastring = wavelength + chiexlower + loggf + vdw + jup + gamrad + lowerorbital + upperorbital + eqw + eqwerr + ' ' + "'" + str(compound + ' ' + comment)
        if (compound not in result.keys()):
            result[compound] = {}
        if (ID not in result[compound].keys()):
            result[compound][ID] = []
        result[compound][ID].append(datastring)

    return result


def extract_atomic_data(data):
    """
    We extract the atomic information from the lines.
    It tries to be clever and find a way to work around the various broken formats of the VALD list
    Returns a list containing either the information if found or None.

    """
    # Doing a bit of cleanup first. There might be some undesirable characters, that we do not need here.
    # There may be a space in the string, with a \ before to protect it.
    # Let's get rid of it, we don't need it.
    if '\\' in data:
        data = data.replace("\\ ", ".")
    if '?' in data:
        data = data.replace('?', '')

    # First try, we assume the line contains all the information, and we can find the three chunks we're looking for.
    try:
        pattern = re.compile("'\s*(\S*)\s+(\S+)\s+(\S*)'")
        result = pattern.search(data)
        members = result.groups()
        if len(members) != 3:
            raise AttributeError
    except AttributeError:
        # One field missing. We will try to find two chunks
        pattern = re.compile("'\s+(\S+)\s+(\S*)'")
        result = pattern.search(data)
        try:
            members = result.groups()
            if len(members) != 2:
                raise AttributeError
        except AttributeError:
            # Two fields failed too, let's try one.
            pattern = re.compile("'\s+(\S*)'")
            result = pattern.search(data)
            try:
                members = result.groups()
            except AttributeError:
                pass
    # Working with a list will allow to change inplace elements of the pattern search
    members = list(members)
    while len(members) != 3:
        members.append('None')

    return members


def build_identification(compound, elements):
    """
    We build here the identification string for each compound, atom or molecule
    This identification has the following format:
    XXYY.WWWZZZ I
    Where :
    XX is the atomic mass of the first element. Replaced by two space if only one element
    ZZ is the atomic mass of the second element
    WWW is the mass of the first element
    ZZZ is the mass of the second element
    I is the ionisation stage of the compound. Equals to 1 for a molecule.
    """
    ID = ''
    atom, ionisation = compound.split(' ')
    if not elements:
        first_mass = '  '
        second_mass = str(periodic_table.index(atom)+1)
        try:
            ion_state_1 = from_roman[ionisation]
        except KeyError:
            ion_state_1 = ''
        ID = first_mass + second_mass + '.000'

    else:
        # compound with isotopes.
        elts = list((elements))
        if elements[3]:
            first_mass = '{0:2d}'.format(periodic_table.index(elts[1])+1)
            second_mass = '{0:02d}'.format(periodic_table.index(elts[4])+1)
            ion_state_1 = '{0:03d}'.format(int(elts[0]))
            ion_state_2 = '{0:03d}'.format(int(elts[3]))
            ID = str(first_mass) + str(second_mass) + '.' + str(ion_state_1) + str(ion_state_2)
        else:
            # We have now the following possibilities:
            # one isotope, such as 6Li or
            # one molecule with either H and another atom (CH, MgH, aso.) or
            # one molecule with only one isotope, as  (48)TiO
            if elts[1] in periodic_table:
                first_mass = '{0:2d}'.format(periodic_table.index(elts[1])+1)
                ion_state_1 = '{0:03d}'.format(int(elts[0]))
                ID = str(first_mass) + '.' + str(ion_state_1)
            elif elts[1][-1] == 'H':
                first_mass = '{0:02d}'.format(periodic_table.index(elts[1][:-1])+1)
                ion_state_1 = '{0:03d}'.format(int(elts[0]))
                second_mass = '{0:2d}'.format(periodic_table.index('H')+1)
                ion_state_2 = '000'
                ID = str(second_mass) + str(first_mass) + '.' + str(ion_state_2) + str(ion_state_1)
            else:
                # It's something like  TiO.
                first_mass = '{0:02d}'.format(periodic_table.index(elts[1][:2])+1)
                ion_state_1 = '{0:03d}'.format(int(elts[0]))
                second_mass = '{0:2d}'.format(periodic_table.index(elts[1][2:])+1)
                ion_state_2 = '000'

                ID = str(second_mass) + str(first_mass) + '.' + str(ion_state_2) + str(ion_state_1)

    return (ID, ionisation)


def get_orbital(configuration):
    structure = configuration.split('.')
    orb = 'X'
    for orbital in structure[::-1]:
        index = -1
        if '(' in orbital:
            continue
        try:
            np.int(orbital[-1])
            index -= 1
        except ValueError:
            pass
        orb = orbital[index]
        return orb
    return orb


def identify_levels(info):
    lowerlevelinfo = info[0]
    upperlevelinfo = info[1]
    lower_level_atomic_info = extract_atomic_data(lowerlevelinfo)
    upper_level_atomic_info = extract_atomic_data(upperlevelinfo)

    # We extract the orbitals from the atomic configuration.
    if 'Hb' in upper_level_atomic_info:
        upper_orbital = 'X'
    else:
        try:
            upper_orbital = get_orbital(upper_level_atomic_info[1])
        except IndexError:
            upper_orbital = 'X'
    if 'Hb' in lower_level_atomic_info:
        lower_orbital = 'X'
    else:
        try:
            lower_orbital = get_orbital(lower_level_atomic_info[1])
        except IndexError:
            lower_orbital = 'X'
    # We also create the comment part of the line that goes into the BSyn format.
    if lower_level_atomic_info[0]:
        comment1 = str(lower_level_atomic_info[0])
    else:
        comment1 = '--'
    if upper_level_atomic_info[0]:
        comment3 = str(upper_level_atomic_info[0])
    else:
        comment3 = '--'

    comment = comment1 + ':' + str(lower_level_atomic_info[1]) + ' ' + comment3 + ':' + str(upper_level_atomic_info[1]) + "'"
    return [lower_orbital, upper_orbital, comment]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Vald2Bsyn')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument(
            '-v',
            '--valdfile',
            help='Name of the file containing the list of lines using the LONG Vald format.',
            required=True
    )
    requiredNamed.add_argument(
            '-b',
            '--bsynfile',
            help='Name of the file where the line list using the BSyn format will be saved',
            required=True
    )
    requiredNamed.add_argument(
            '-e',
            '--extract_type',
            help='Stellar or all',
            required=True
    )
    arguments = parser.parse_args()

    vald2bsyn()
