import numpy as np
import csv
import sys
import os

def combine_csv(data_directory, output):
    """ Combines all the data files in a directory Uses first csv file's header"""

    # get the list of csvs in the directory
    list_of_csv = []
    for file in os.listdir(data_directory):
        list_of_csv.append(file)
    print(list_of_csv)

    header = []
    # just get the header of input1 as list header
    with open(output, 'w') as out:
        csvwriter = csv.writer(out)
        # get header and write all contents of first csv to output
        with open(list_of_csv[0], 'r') as csv1:
            for linenum, line in enumerate(csv1):
                if linenum == 0:
                    header = line.split(',')
                    # filter out \r and \n
                    header = [s.replace("\r", "") for s in header]
                    header = [s.replace("\n", "") for s in header]
                out.writelines(line)

        # for all the other csv files, check header and append to the output file
        for csv_file in list_of_csv[1:]:
            print(csv_file)
            corresponding_index_list = []
            with open(csv_file, 'r') as csv2:
                for linenum, line in enumerate(csv2):
                    # first number, match header with header from input1
                    line = line.split(',')
                    line = [s.replace("\n", "") for s in line]
                    line = [s.replace("\r", "") for s in line]
                    # initiate values of zeros
                    values = np.zeros(len(line))
                    if linenum == 0:
                        for heading in line:
                            # this will error if the columns are different
                            corresponding_index_list.append(header.index(heading))
                    else:
                        for index, value in enumerate(line):
                            write_index = corresponding_index_list[index]
                            values[write_index] = value
                        csvwriter.writerow(values)

    with open(output, 'r') as out:
        for linenum, line in enumerate(out):
            if linenum == 0:
                column_num = len(line.split(','))

            if len(line.split(',')) != column_num:
                print('This is wrong, number of columns is not consistant')
                raise ValuesError()


combine_csv(sys.argv[1], sys.argv[2])