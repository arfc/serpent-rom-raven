import h5py
file = '../serpent-raven/db_saltproc.hdf5'
f = h5py.File(file, 'r')
iso = f['iso_codes'][:]
with open('iso_file', 'w') as out:
    for i in iso:
        print(i.decode('utf-8'))
        out.write(i.decode('utf-8') +'\n')