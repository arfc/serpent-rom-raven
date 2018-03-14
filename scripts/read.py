import h5py
import numpy as np
import csv
import sys

def read_hdf5(filename):
    f = h5py.File(filename, 'r')

    for key in f:
        print(key)
        print(f[key])

def read_csv(filename):
    with open(filename, mode='r') as input_file:
        for i, line in enumerate(input_file):
            if i == 0:
                header = line.split(',')
            if i == 1:
                value = line.split(',')
    for i in range(len(header)):
        if float(value[i].strip()) != 0:
            print('%s : %s \n' %(header[i], value[i]))

read_csv(sys.argv[1])