#Creates a sky map with ICRS standards from a singular .csv file
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from astropy import units as u
from astropy.coordinates import (SkyCoord, Distance, Galactic, 
                                 EarthLocation, AltAz)
import astropy.coordinates as coord
from astropy.io import fits
from astropy.table import QTable
from astropy.time import Time
from astropy.utils.data import download_file

#file to be converted put here
print("Enter file address (with .csv at the end):")
local_data_filename = input()
f = h5py.File(local_data_filename, 'r')

#Read Catalogue
tbl = QTable.read(f)
objects = SkyCoord(
    ra=tbl['RAJ2000'],
    dec=tbl['DECJ2000'],
    frame='icrs',
    unit=(u.deg, u.deg))

#Create the plot
def coordinates_aitoff_plot(coords):
    fig, ax = plt.subplots(figsize=(10, 4), 
                           subplot_kw=dict(projection="aitoff"))
    
    sph = coords.spherical
    cs = ax.scatter(-sph.lon.wrap_at(180*u.deg).radian,
                    sph.lat.radian)

    def fmt_func(x, pos):
        val = coord.Angle(-x*u.radian).wrap_at(360*u.deg).degree
        return f'${val:.0f}' + r'^{\circ}$'

    ticker = mpl.ticker.FuncFormatter(fmt_func)
    ax.xaxis.set_major_formatter(ticker)

    ax.grid()
    
    return fig, ax

#Display plot from catalogue
fig, ax = coordinates_aitoff_plot(objects)
ax.set_xlabel('RA [deg]')
ax.set_ylabel('Dec [deg]')

#Saves to file name
print("Enter new file name (with .png at the end):")
name = input()
plt.savefig(name)

f.close()
print("Done")