#!/usr/bin/python
# -*- coding: utf-8 -*-

# Python imports
import sys
import argparse

# import datetime

# Numpy imports
# import numpy as np

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


def vald2bsyn():
    # First, we read the VALD file.
    valddata = readvald(arguments.valdfile)


def readvald(valdfile):
    with open(valdfile, 'r') as f:
        linedata = []
        index = 1
        for line in f:
            # Let's filter first all lines in the file that are not line data. These lines do not start with a single quote
            if not line.startswith(("'")):
                print('header {0}'.format(line))
                continue
            # We are now reading the details of each line. Information is spread over 3 lines.
            print('index : {0}'.format(index % 3))
            if index < 3: 
                # print(linedata)
                linedata.append(line)
                index += 1
            else:
                index = 0
        print(linedata)


    return linedata


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
