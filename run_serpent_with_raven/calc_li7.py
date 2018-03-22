import mass_frac_calc
def evaluate(self):
    key = __file__.split('_')[1]
    key = key.split('.')[0]
    return mass_frac_calc.return_value(key, self.u233_mole_frac)