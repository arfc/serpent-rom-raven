# SERPENT-RAVEN ROM GENERATION

### serpent-raven
This is where the input serpent files are.
All RAVEN runs regarding SERPENT-RAVEN interface
are pointed to this directory (WorkingDir).

### rom
This folder contains the ROM generated and tests to validate
the ROM. All RAVEN runs regarding using or generating the ROM
are pointed to this directory (WorkingDir)


### scripts
This directory contains all scripts to curate hdf5 data
received from Andrei (@andrewryh0) or generate isotopic
files (list of isotopes that the ROM would track)

### doc
This folder has a report in LaTex describing the process
of generating SERPENT ROM with RAVEN. Execute `make` in this
directory to compile into pdf.

### SerpentInterface.py
This python script is the interface for RAVEN and SERPENT.
This file should be in the RAVEN repository in path
`..../raven/framework/CodeInterfaces/SERPENT/`.
 