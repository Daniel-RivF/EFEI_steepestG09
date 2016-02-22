#!/usr/bin/python
import glob, os, time, shutil, re
import tools_EFEI as tools

#first_file = raw_input(' Filename of the g09 first output (for now, im just working with g09 CASSCF gradient calculations)')
#route_sect = raw_input(' Enter route section (including #p): \n')
#charge = raw_input(' Charge?\n')
#spin = raw_input(' Spin multiplicity? \n')
#atom1 = int(raw_input('First pulling point (atom label)\n') ) 
#atom2 = int(raw_input('Second pulling point (atom label)\n') )
#modF = float(raw_input('Force pair value (for one atom)\n'))
#elongation = int(raw_input('Tip 1 for elongation and -1 for compression\n'))
#step = float(raw_input('Enter the step value: \n'))
#maxsteps = int(raw_input('Maximum number of steps:\n '))




first_file = 'stp.log'
route_sect ='#p CASSCF(4,4,NRoot=2,StateAverage)/6-31g* Nosymm \n# GFInput pop=full force SCF=(MaxCycle=300,conver=7) guess=read'
charge = 0
spin = 1
atom1 = 5
atom2 = 8
modF = 1.0
elongation = 1 
step = 0.2
maxsteps = 999 




basename = os.path.splitext(first_file)[0] 


points_list = ["%04d" % x for x in range(maxsteps)]
filenames_out_list = [ basename + '.efei.' + j + '.log' for j in points_list]
filenames_inp_list = [ basename + '.efei.' + j + '.com' for j in points_list]

firstname = basename + '.efei.' + points_list[0] + '.log'
shutil.copy(first_file,firstname)
chk_0 = os.path.splitext(first_file)[0] + '.chk'
first_namechk = re.sub('[._-]', '',os.path.splitext(firstname)[0]) + '.chk'
shutil.copy(chk_0,first_namechk)




for i in points_list :
    filei = basename + '.efei.' + i +  '.log'
    print filei
    while not os.path.exists(filei):
        time.sleep(10)
    if not tools.Check_termination(filei):
        break
    else:
        Z=tools.parsexyz(filei)[0]
        fvector = tools.construct_fvector(filei,atom1,atom2,modF,elongation)
        new_xyz = tools.new_xyzvector(filei,fvector,step)
        next_point = points_list[1+points_list.index(i)]
        inp_name = basename + '.efei.' + next_point + '.com'
        chk_old = re.sub('[._-]', '',os.path.splitext(filei)[0]) + '.chk'
        chk_new = re.sub('[._-]', '',os.path.splitext(inp_name)[0]) + '.chk'
        shutil.copy(chk_old,chk_new)
        tools.new_input(inp_name,route_sect,charge,spin,Z,new_xyz)  
        os.system('Launch_gaussian %s' % inp_name)
            # Write it, and launch it 

        





#if os.path.isfile(
#
#fvector = construct_fvector(filename,atom1,atom2,modF,elongation)
#newxyz = tools.new_xyzvector(filename,fvector,step)
#name_new_input = 
