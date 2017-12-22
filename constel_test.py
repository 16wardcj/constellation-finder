"""Print constellation.

Command line arguments:
cons_bounds_f -- filepath to constellation boundary data

Runtime arguments:
RA -- right-ascension given in HH.hhhh...
DEC -- declination given in DD.dddd...
"""

import sys
import pandas as pd

import constel

cons_bounds_f = sys.argv[1]

cons_bounds = pd.read_table(cons_bounds_f, delim_whitespace=True, names=["ra", "dec", "con", "i/o"])

while True:
    ra = float(input("RA: "))
    dec = float(input("DEC: "))

    print("Is in constellation: ", constel.find_constel(ra, dec, cons_bounds))
