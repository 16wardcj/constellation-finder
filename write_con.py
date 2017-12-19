import sys
import pandas as pd

"""
input:
    cons.csv - filepath to constellation boundary data
    objects.csv - filepath to objects csv file
    results_dir_filepath - filepath to directory which will contain constellation files

output:
    results_filepath/___.csv - folder containing all objects sorted by constellation
"""

con_bounds_f = sys.argv[1]
objs_f = sys.argv[2]
res_dir = sys.argv[3]

con_bounds = pd.read_table(con_bounds_f, delim_whitespace=True, names=["ra", "dec", "con", "i/o"])
objs = pd.read_csv(objs_f, index_col=0)

for con in con_bounds["con"].unique():
    res = objs.loc[objs["con"].str.contains(con)] # substring test required because of boundary cases

    res.to_csv("%s%s.csv" % (res_dir, con), columns=["pl_hostname", "pl_letter", "con"], index=False)
