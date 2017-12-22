# constellations-exoplanets

This repository contains a Python script (constel.py) which determines the constellation an object is contained within given its coordinates in right-ascension and declination.

The data file used for the constellation boundaries is bound_20.dat (Vizier VI/49). The file containing the stellar objects of interest is planets.csv (NASA exoplanet archive) although any tabulated file with right-ascension and declination coordinates could be made to work.

A program with the same purpose was written in Fortran and C (Roman 1987 - Vizier VI/42). In order for it to work  it required user input during the execution of the program making it less suitable for bulk analysis. It also calculated the precession of the stellar coordinates back to 1875 so as to use a specialist table. The program in this repository works with the most recent boundary files and does not need to calculate any precession.
