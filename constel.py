"""Module that identifies constellation from stellar coordinates.

Functions:
find_constel -- return constellation name
run -- perform find_constel for a table of stellar objects
"""

import pandas as pd

def find_constel(ra, dec, con_bounds):
    """Return constellation name.

    Keyword arguments:
    ra -- right-ascension in HH.hhhh...
    dec -- declination in DD.dddd...
    con_bounds -- pandas DataFrame with constellation boundary info

    Note that if the object lies on the boundary of two constellations XXX and YYY the result returned will be 'XXX+YYY'.
    """
    result = ""

    for con in con_bounds["con"].unique():
        con_coords = con_bounds.loc[con_bounds["con"] == con]

        intersects = 0
        on_boundary = False

        for i in range(con_coords.shape[0]):
            l_coord = con_coords.iloc[i-1]
            r_coord = con_coords.iloc[i]

            if r_coord["ra"] < l_coord["ra"]:
                l_coord, r_coord = r_coord, l_coord

            # check if coord pair cross ra = 0
            is_crossing = False

            if r_coord["ra"] - l_coord["ra"] > 5:
                is_crossing = True

            # check if exoplanet coord lies between coord pair
            if not is_crossing:
                if ra < l_coord["ra"] or r_coord["ra"] <= ra:
                    continue
            else:
                if l_coord["ra"] <= ra and ra < r_coord["ra"]:
                    continue

            # check if coord pair is above exoplanet coord
            if dec <= l_coord["dec"] and dec <= r_coord["dec"]:
                intersects += 1

            # check if exoplanet coord is on boundary
            elif l_coord["dec"] < dec and dec <= r_coord["dec"]:
                on_boundary = True

            elif r_coord["dec"] < dec and dec <= l_coord["dec"]:
                on_boundary = True

        # check if exoplanet coord is on a boundary
        if on_boundary:
            if result == "":
                result = con
            else:
                result += "+" + con
            continue

        # check if odd no of intersections
        if intersects % 2 == 1:
            result = con
            break

    # check if coord is in UMI near Polaris (region not entirely covered)
    if result == "" and dec > 85:
        result = "UMI"

    return result

def run(con_bounds_f, objs_f, res_f):
    """Save a .csv file with original stellar object info plus an additional constellation column.

    Keyword arguments:
    con_bounds_f -- constellation boundary filename
    objs_f -- stellar objects filename
    res_f -- .csv output filename
    """

    con_bounds = pd.read_table(con_bounds_f, delim_whitespace=True, names=["ra", "dec", "con", "i/o"])
    objs = pd.read_csv(objs_f, index_col=0, comment="#")

    # convert ra in objs from degrees to hours
    objs["ra"] *= 24/360

    for i, obj in objs.iterrows():
        print("%d of %d" % (i, objs.shape[0]))
        objs.at[i, "con"] = find_constel(obj["ra"], obj["dec"], con_bounds)

    objs.to_csv(res_f)
