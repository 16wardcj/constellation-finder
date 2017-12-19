import find_con

import sys
import pandas as pd

cons_bounds_f = sys.argv[1]

cons_bounds = pd.read_table(cons_bounds_f, delim_whitespace=True, names=["ra", "dec", "con", "i/o"])

while True:
    ra = float(input("RA: "))
    dec = float(input("DEC: "))

    print("Is in constellation: ", find_con.find_con(ra, dec, cons_bounds))
