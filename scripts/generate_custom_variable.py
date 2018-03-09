file = '../iso_file'
isotopes = []
with open(file, 'r') as isofile:
    for line in isofile:
        isotopes.append(line.strip())

custom_variable_file = '../custom_xml'
with open(custom_variable_file, 'w') as cvf:
    for iso in isotopes:
        print(iso)
        cvf.write('<variable name="f' + iso + '"/> \n')
