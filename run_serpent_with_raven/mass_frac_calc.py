def return_value(key, u233_mole_frac):
    mole_frac_dict = {'thf4': 12,
                      'bef2': 16}

    # u233_mole_frac should range from 0.2 to 0.3 percent.
    mole_frac_dict['uf4'] = u233_mole_frac
    mole_frac_dict['lif'] = 100 - mole_frac_dict['thf4'] - mole_frac_dict['bef2'] - mole_frac_dict['uf4']

    # change to fraction
    mole_frac_dict = {k: v / 100.0 for k,v in mole_frac_dict.iteritems() }

    # composition of li7 and li6 in lithium
    li7_iso_frac = 0.999952
    li6_iso_frac = 1 - li7_iso_frac

    print(mole_frac_dict.values())
    mass_dict = {}
    mass_dict['li7'] = (mole_frac_dict['lif']) * li7_iso_frac * 7.016 
    mass_dict['li6'] = (mole_frac_dict['lif'])  * li6_iso_frac * 7.016
    mass_dict['f19'] = (
                       (mole_frac_dict['lif']) * 19
                     + (mole_frac_dict['bef2']) * 2 * 19
                     + (mole_frac_dict['thf4']) * 4 * 19
                     + (mole_frac_dict['uf4']) * 4 * 19
                     )
    mass_dict['be9'] =  (mole_frac_dict['bef2']) * 9.0121
    mass_dict['th232'] = (mole_frac_dict['thf4']) * 232.038
    mass_dict['u233'] = (mole_frac_dict['uf4']) * 233.0396
    print(mass_dict.values())
    total_mass = sum(mass_dict.itervalues())

    mass_frac_dict = {k: v / total_mass * 100.0 * -1 for k, v in mass_dict.iteritems() }

    return mass_frac_dict[key]