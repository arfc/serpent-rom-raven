import sys
sys.path.append("/projects/sciteam/bahg/projects/raven/scripts")
from externalROMloader import ravenROMexternal
import numpy as np 


rom = ravenROMexternal("/projects/sciteam/bahg/projects/raven/framework/CodeInterfaces/SERPENT/test/rom/keff_rom_svm.pk",
                       "/projects/sciteam/bahg/projects/raven/raven_framework")


with open('../rom/test_input.csv', 'r') as out:
    lines = f.readlines()
    print(lines)
