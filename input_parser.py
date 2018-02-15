def read_input_file(filename):
    keyword_dict = {}
    fileobject = open(filename)
    lines = fileobject.readlines()
    current_section = ''
    mat_beg = False
    # comp_dict stores composition of different materials
    # key: isotope  /// value: fraction
    comp_dict = {}
    # dense_dict stores the total density of the simulation
    # stores tuples (density, atom or mass)
    dense_dict = {}
    for line in lines:
        if line[0] == '%' or line.isspace():
            x = 0
        else: 
            print(line)
            # filter out the comments in the same line
            if line.find('%') != -1:
                line = line[:line.find('%')]
            
            # beginning of material definition
            if 'mat' in line:
                current_section = 'mat'
                # split by whitespace to get material name
                temp = line.split()
                # if negative value for <dens>,
                # mass density. Atom density if positive
                if temp[2][0] == '-':
                    atom_or_mass = 'mass'
                else:
                    atom_or_mass = 'atom'
                # material dictionary with key material name
                # value: dictionary (key: isotope, value: atomic density)
                key = temp[1] + ' ' + atom_or_mass
                comp_dict[key] = {}
                dense_dict[key] = (abs(float(temp[2])), atom_or_mass)

            elif 'therm' in line:
                current_section = 'therm'

            elif 'set' in line:
                current_section = 'set'

            elif 'dep' in line:
                current_section = 'dep'

            elif current_section == 'mat':
                if line.split()[0] == 'rgb':
                    # whatis this rgb
                    print('what is this rgb')
                else:
                    isotope, fraction = get_isotope_frac_list(line)
                    comp_dict[key][isotope] = abs(float(fraction)) 

    for key in dense_dict:
        print('Total:')
        print(dense_dict[key])
        print(key)
        print(comp_dict[key])
        
def get_isotope_frac_list(line):
    """ Convert a line of material definition into
        list of parsed isotope and fraction

    Parameters
    ----------
    line: str
        string of isotope and fraction (eg. 3007.09c  0.00)

    Returns
    -------
    isotope: int
        isotope number
    fraction: float
        fraction of that isotope in material
    """

    split_list = line.split()
    isotope = int(split_list[0][:-4])
    fraction = split_list[1]
    return isotope, fraction

read_input_file('./input/publ_core')