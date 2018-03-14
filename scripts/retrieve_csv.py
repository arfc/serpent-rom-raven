import numpy as np
import sys
sys.path.append("../../scripts")
import csv
import output_parser as op

""" If you lost your outpoint dump csv, put this in the runGrid folder and run it"""

iso_list = op.read_file_into_list('../../iso_file')

with open('retrieved.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    header_list = (['f'+iso for iso in iso_list] +
              ['boc_keff', 'eoc_keff', 'deptime'] +
              ['d'+iso for iso in iso_list]) 
    writer.writerow(header_list)

    for i in range(1681):
        if i == 0:
            # skip 0
            continue
        path = '%i/msbr_input_comp.serpent'%i
        
        res = path + "_res.m"
        inbumat = path + ".bumat0"
        outbumat = path + ".bumat1"
        input_file = path


        deptime = op.find_deptime(input_file)
        keff_dict = op.search_keff(res)
        boc_keff = keff_dict['keff'][0]
        eoc_keff = keff_dict['keff'][1]
        in_bumat_dict = op.bumat_read(inbumat, 1e-7)
        out_bumat_dict = op.bumat_read(outbumat, 1e-7)
        
        fresh_adens_list = [0] * len(iso_list)
        dep_adens_list = [0] * len(iso_list)
        for key in in_bumat_dict:
            if key in iso_list:
                index = iso_list.index(key)
                fresh_adens_list[index] = in_bumat_dict[key]
        for key in out_bumat_dict:
            if key in iso_list:
                index = iso_list.index(key)
                dep_adens_list[index] = out_bumat_dict[key]
        row = fresh_adens_list + [boc_keff, eoc_keff, deptime] + dep_adens_list
        writer.writerow(row)

