import sys
sys.path.append("/projects/sciteam/bahg/projects/raven/scripts")
from externalROMloader import ravenROMexternal
import numpy as np 


rom = ravenROMexternal("/projects/sciteam/bahg/projects/raven/framework/CodeInterfaces/SERPENT/test/rom/keff_rom_svm.pk",
                       "/projects/sciteam/bahg/projects/raven/framework")


with open('../rom/test.csv', 'r') as out:
    lines = out.readlines()
    keys = lines[0].split(',')
    values = lines[1].split(',')
    dic = {}
    for i in range(len(keys)):
        if '\n' in keys[i]:
            keys[i] = keys[i].replace('\n','')
        dic[keys[i]] = [float(values[i])]
    print(dic)

eval = rom.evaluate(dic)
print(eval)