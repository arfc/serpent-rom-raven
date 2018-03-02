import h5py
import numpy as np

filename = 'db_saltproc.hdf5'
f = h5py.File(filename, 'r')
out = h5py.File('db_modified.hdf5', 'w')


# core adensity before reproc is the depleted composition
# of previous step
dep_comp = f['core adensity before reproc'][1:]

# core adensity after reproc is the fresh composition
# that gets depleted in the simulation
fresh_comp = f['core adensity after reproc'][:-1]

keff = f['keff'][0]

# move the depleted fuel one before to match fresh and depleted composition
out.create_dataset('dep_comp', data=dep_comp)
out.create_dataset('fresh_comp', data=fresh_comp)

# keff dataset
out.create_dataset('keff', data=keff)
# have an array of 3 (days) for deptime
out.create_dataset('deptime', data=np.linspace(3,3, len(dep_comp)))


out.close()
# check if done properly
n = h5py.File('db_modified.hdf5', 'r')

for key in n:
    print(key)
    print(n[key])