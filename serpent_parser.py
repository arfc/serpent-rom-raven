import numpy as np
import csv


def parse_line(line):
    """parse composition line by deleting whitespace
       and separating the isotope and atomic density

    Parameters
    ----------
    line: str
        line of isotope and composition

    Returns
    -------
    tuple : (str, float)
        (isotope, atomic density)
    """
    
    # remove whitespace in front
    line = line.lstrip()
    isotope, atom_density = line.split("  ")
    return (isotope, float(atom_density))


def filter_trace(comp_dict, percent_cutoff):
    """filters isotopes with less than percent_cutoff
       for easier calculation

    Parameters
    ----------
    comp_dict: dictionary
        key=isotope
        value=atomic density
    percent_cutoff:

    Returns
    -------
    filtered dictionary
        key=isotope
        value=atomic density
    """
    # check if percent_cutoff value is valid
    if percent_cutoff < 0 or percent_cutoff > 100:
        raise ValueError('Percent has to be between 0 and 100')

    # calculate atomic_density_cutoff
    total_atomic_density = sum(comp_dict.values())
    atomic_density_cutoff = percent_cutoff * total_atomic_density / 100

    # delete list since cannot change dictionary during iteration
    delete_list = []
    for key, atom_density in comp_dict.items():
        if atom_density < atomic_density_cutoff:
            delete_list.append(key)

    # delete the isotopes with less than percent_cutoff
    for isotope in delete_list:
        del comp_dict[isotope]


    return comp_dict



def bumat_read(filename):
    """reads serpent .bumat output file and 
       stores the composition in a dictionary

    Parameters
    ----------
    filename: str
        bumat file path

    Returns
    -------
    dict
        dictionary of composition
        (key=isotope(ZZAAA), value=atomic density)
    """
    with open(filename) as f:
        useful = f.readlines()[5:]

    comp_dict = {}
    header = useful[0]
    for i in range(1, len(useful)):
        parsed = parse_line(useful[i])
        # isotope as key, atomic density as value
        comp_dict[parsed[0]] = parsed[1]

    comp_dict = filter_trace(comp_dict, 0.01)
    return comp_dict


def csv_render(csv_filename, dictionary):
    """renders csv given the dictionary
       column 1 = key, column 2 = value
    
    Parameters
    ----------
    csv_filename: str
        path of csv file to be created
    dictionary: dict
        dictionary to be rendered into csv file

    Returns
    -------
    true if successful.
    """
    with open(csv_filename, 'w') as csv_file:
        writer = csv.writer(csv_file)
        # write header
        writer.writerow(['Isotope', 'Atomic Density'])
        for key, value in dictionary.items():
            writer.writerow([key, value])

    return True

comp_dict = bumat_read('./output/publ_core.bumat1')
csv_render('composition.csv', comp_dict)