import h5py
import numpy as np
import csv
import os

# this bit converts andrei's hdf5 to more relevant format

saltproc_file = '../serpent-raven/db_saltproc.hdf5'
f = h5py.File(saltproc_file, 'r')
try:
    os.remove('../serpent-raven/db_modified.hdf5')
except:
    print('no db modified')
modified_hdf5 = h5py.File('../serpent-raven/db_modified.hdf5', 'w')


# core adensity before reproc is the depleted composition
# of previous step
dep_comp = f['core adensity before reproc'][1:]

# core adensity after reproc is the fresh composition
# that gets depleted in the simulation
fresh_comp = f['core adensity after reproc'][:-1]

boc_keff = f['keff_BOC'][0]
eoc_keff = f['keff_EOC'][0]

iso_codes = f['iso_codes'][:]
iso_codes = [x.decode('utf-8') for x in iso_codes]

# put duplicate indeces in no-do list:
no_do_list = []
for iso in iso_codes:
    indeces = [i for i, x in enumerate(iso_codes) if x == iso]
    if len(indeces) != 1:
        for index in indeces[1:]:
            no_do_list.append(index)
no_do_list = list(set(no_do_list))

# move the depleted fuel one before to match fresh and depleted composition
modified_hdf5.create_dataset('dep_comp', data=dep_comp)
modified_hdf5.create_dataset('fresh_comp', data=fresh_comp)

# keff dataset
modified_hdf5.create_dataset('boc_keff', data=boc_keff)
modified_hdf5.create_dataset('eoc_keff', data=eoc_keff)
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
fresh_comp = f['fresh_comp']

dep_comp_filtered = np.empty(len(dep_comp[0]) - len(no_do_list))
fresh_comp_filtered = np.empty(len(dep_comp[0]) - len(no_do_list))
iso_codes_filtered = np.empty(len(dep_comp[0]) - len(no_do_list))
# delete duplicate isotopes
for i in range(len(boc_keff)):
    dep_comp_filtered = np.vstack((dep_comp_filtered,
                                  np.delete(dep_comp[i], no_do_list)))
    fresh_comp_filtered = np.vstack((fresh_comp_filtered,
                                    np.delete(fresh_comp[i], no_do_list)))
iso_codes_filtered = np.delete(iso_codes, no_do_list)

print(len(dep_comp_filtered[0]))


# keff[0] is the keff value of dep_comp[0]
boc_keff = f['boc_keff']
eoc_keff = f['eoc_keff']
deptime = [3] * len(boc_keff)

with open(outfile, 'w') as csv_file:
    writer = csv.writer(csv_file)
    fresh = ['f' + str(x) for x in iso_codes_filtered]
    dep = ['d' + str(x) for x in iso_codes_filtered]
    header_list = fresh + ['boc_keff', 'eoc_keff', 'deptime'] + dep
    # header is inputisotopes - keff - deptime - depisotopes
    writer.writerow(header_list)
    for i in range(len(boc_keff)):
        row_list = np.append(fresh_comp_filtered[i], boc_keff[i])
        row_list = np.append(row_list, eoc_keff[i])
        row_list = np.append(row_list, deptime[i])
        row_list = np.append(row_list, dep_comp_filtered[[i]])
        #row_list = fresh_comp[i] + [keff[i], deptime[i]] + dep_comp[i]
        if i == 0:
            print(len(row_list))
            print(len(header_list))
        writer.writerow(row_list)



