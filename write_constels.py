"""Convert processed stellar objects .csv file into one file per constellation.

Command line arguments:
cons_bounds_f -- filepath to constellation boundary data
objs_f - filepath to objects .csv file
res_dir - filepath to directory which will contain constellation files

Output:
res_dir/XXX.csv - folder containing objects sorted by constellation

Eg:
python write_constels.py bound_20.dat objects.csv objects/
"""

import sys
import pandas as pd

con_bounds_f = sys.argv[1]
objs_f = sys.argv[2]
res_dir = sys.argv[3]

con_bounds = pd.read_table(con_bounds_f, delim_whitespace=True, names=["ra", "dec", "con", "i/o"])
objs = pd.read_csv(objs_f, index_col=0)

for con in con_bounds["con"].unique():
    res = objs.loc[objs["con"].str.contains(con)] # substring test required because of boundary cases

    res.to_csv("%s%s.csv" % (res_dir, con), columns=["pl_hostname", "pl_letter", "con"], index=False)
