"""Plot the boundary of a constellation in either cartesian or polar coordinates. Useful for visualising.

Command line arguments:
cons_name1 -- abbreviated name of first constellation
cons_name2 -- abbreviated name of second constellation

Output:
Displays a graph.

Eg:
python plot_constel.py UMI CEP

Notes:
Polar coordinates are most suitable for constellations near the north and south poles. Use cartesian coordinates for constellations nearer the equator.
To alternate between cartesian and polar coordinates comment out the appropriate line of code at the end of the file.
"""

import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_cartesian(cons_coords):
    plt.plot(cons_coords[0]["ra"], cons_coords[0]["dec"])
    plt.plot(cons_coords[1]["ra"], cons_coords[1]["dec"])

    plt.show()

def plot_circular(cons_coords):
    plt.polar(cons_coords[0]["ra"]*np.pi/12, 90-abs(cons_coords[0]["dec"]))
    plt.polar(cons_coords[1]["ra"]*np.pi/12, 90-abs(cons_coords[1]["dec"]))

    plt.show()

cons_name1 = sys.argv[1]
cons_name2 = sys.argv[2]

cons_bounds = pd.read_table("./bound_20.dat", delim_whitespace=True, names=["ra", "dec", "con", "i/o"])

cons_coords1 = cons_bounds.loc[cons_bounds["con"] == cons_name1]
cons_coords2 = cons_bounds.loc[cons_bounds["con"] == cons_name2]

plot_cartesian((cons_coords1, cons_coords2))
#plot_circular((cons_coords1, cons_coords2))
