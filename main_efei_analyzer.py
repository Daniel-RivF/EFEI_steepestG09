#!/usr/bin/python
import glob, os, time, shutil, re
import tools_EFEI as tools
import tools_analysis_efei as tools_usr

first_file = 'stp.log'
#calculation_type = raw_input('Type casscf or dft : ')
#relaxed root = raw_input('Type the #Root where the gradient was computed (1 for the ground state):  ')
calculation_type = 'casscf'
rlxroot = 2
atom1 = 5
atom2 = 8
modF = 1.0
elongation = 1 
step = 0.2
# atom indexes for coordinates
arguments= = [ [5,8],[1,7,13,8],[4,8,7,14],[4,5,6,11],[5,6,12,1],[6,7] ]

#for i in $(ls -d ???/); do j=${i%?}; cp $j/optFext.log ../stp.efei.${j}.log; done
lista_f = sorted(glob.glob('*log'))
geoms = tools.readgeoms(listaf)
fout = os.path.splitext(first_file)[0] + '.PATH.xyz'
xyz_writer(lista_f,fout)






for coord in arguments:
    tools_usr.check_internal(geoms,argument)
tools_usr.check_internal(geoms,argument)


