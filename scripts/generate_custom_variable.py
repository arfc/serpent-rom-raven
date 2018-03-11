file = '../iso_file'
isotopes = []
with open(file, 'r') as isofile:
    for line in isofile:
        isotopes.append(line.strip())

custom_variable_file = '../custom_xml'
with open(custom_variable_file, 'w') as cvf:
    for iso in isotopes:
        cvf.write('<variable name="f' + iso + '"/> \n')

feature_space = '../feature_space'
with open(feature_space, 'w') as fs:
    for iso in isotopes:
        fs.write('f'+iso+',')

target_space = '../target_space'
with open(target_space, 'w') as ts:
    for iso in isotopes:
        ts.write('d'+iso+',')