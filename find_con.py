import sys
import pandas as pd

"""
WRITE PROPERLY
input:
    constellation boundaries filepath (from Vizier)
    objects filepath (from NASA exoplanet archives)
    output filename

output:
    objects.csv (same as objects input but added column of constellation)

eg:
"""

def find_con(ra, dec, con_bounds):
    """
    DOCSTRING
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

if __name__ == "__main__":
    con_bounds_f = sys.argv[1]
    objs_f = sys.argv[2]
    res_f = sys.argv[3]

    con_bounds = pd.read_table(con_bounds_f, delim_whitespace=True, names=["ra", "dec", "con", "i/o"])
    objs = pd.read_csv(objs_f, index_col=0, comment="#")

    # convert ra in objs from degrees to hours
    objs["ra"] *= 24/360

    for i, obj in objs.iterrows():
        print("%d of %d" % (i, objs.shape[0]))
        objs.at[i, "con"] = find_con(obj["ra"], obj["dec"], con_bounds)

    objs.to_csv(res_f)
