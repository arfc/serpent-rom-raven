import h5py
import numpy as np
import csv


# this bit converts andrei's hdf5 to more relevant format

saltproc_file = '../serpent-raven/db_saltproc.hdf5'
f = h5py.File(saltproc_file, 'r')
modified_hdf5 = h5py.File('../serpent-raven/db_modified.hdf5', 'w')


# core adensity before reproc is the depleted composition
# of previous step
dep_comp = f['core adensity before reproc'][1:]

# core adensity after reproc is the fresh composition
# that gets depleted in the simulation
fresh_comp = f['core adensity after reproc'][:-1]

keff = f['keff_BOC'][0]

iso_codes = f['iso_codes'][:]
iso_codes = [x.decode('utf-8').split('.')[0] for x in iso_codes]

# move the depleted fuel one before to match fresh and depleted composition
modified_hdf5.create_dataset('dep_comp', data=dep_comp)
modified_hdf5.create_dataset('fresh_comp', data=fresh_comp)

# keff dataset
modified_hdf5.create_dataset('keff', data=keff)
# have an array of 3 (days) for deptime
modified_hdf5.create_dataset('deptime', data=np.linspace(3,3, len(dep_comp)))
modified_hdf5.close()


#########################################################
# this bit converts hdf5 to csv where each row is one SERPENT run.

filename = '../serpent-raven/db_modified.hdf5'
outfile = '../serpent-raven/modified.csv'
f = h5py.File(filename, 'r')


# dep_comp[0] would be 1158 isotopes for the first depletion
dep_comp = f['dep_comp']
print(type(dep_comp))
fresh_comp = f['fresh_comp']
# keff[0] is the keff value of dep_comp[0]
keff = f['keff']
deptime = [3] * len(keff)

with open(outfile, 'w') as csv_file:
    writer = csv.writer(csv_file)
    fresh = ['f' + str(x) for x in iso_codes]
    dep = ['d' + str(x) for x in iso_codes]
    header_list = fresh + ['keff', 'deptime'] + dep
    # header is inputisotopes - keff - deptime - depisotopes
    writer.writerow(header_list)
    for i in range(len(keff)):
        row_list = np.append(fresh_comp[i], keff[i])
        row_list = np.append(row_list, deptime[i])
        row_list = np.append(row_list, dep_comp[[i]])
        #row_list = fresh_comp[i] + [keff[i], deptime[i]] + dep_comp[i]
        if i == 0:
            print(fresh_comp[i])
            print(keff[i])
            print(deptime[i])
            print(dep_comp[i])
            print(row_list)
        writer.writerow(row_list)



