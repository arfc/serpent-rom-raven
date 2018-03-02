import h5py
import numpy as np

filename = 'db_modified.hdf5'
f = h5py.File(filename, 'r')

for key in f:
    print(key)
    print(f[key])