
import glob, os, time
import tools_EFEI as tools

first_file = raw_input(' Filename of the g09 first output (for now, im just working with g09 CASSCF gradient calculations)')
atom1 = int(raw_input('First pulling point (atom label)') ) 
atom2 = int(raw_input('Second pulling point (atom label)') )
modF = float(raw_input('Force pair value (for one atom)'))
elongation = int(raw_input('Tip 1 for elongation and -1 for compression'))
step = float(raw_input('Enter the step value: '))
maxsteps = int(raw_input('Maximum number of steps: '))


basename = os.path.splitext(first_file)[0] 


points_list = ["%04d" % x for x in range(maxsteps)]
filenames_out_list = [ basename + '.efei.' + j + '.log' for j in points_list]
filenames_inp_list = [ basename + '.efei.' + j + '.com' for j in points_list]
firstname = basename + '.efei.' + points_list[0] + '.log'

for i in points_list :
    filei = basename + '.efei.' + i +  '.log'
    while not os.path.exists(filei):
        time.sleep(15)
    if os.path.exists(filei):
        fvector = tools.construct_fvector(filei,atom1,atom2,modF,elongation)
        new_xyz = tools.new_xyzvector(filei,fvector,step)
        next_point = points_list[1+points_list.index(i)]
        inp_name = basename + '.efei.' + next_point + '.com'
        # Write it, and launch it 

        





#if os.path.isfile(
#
#fvector = construct_fvector(filename,atom1,atom2,modF,elongation)
#newxyz = tools.new_xyzvector(filename,fvector,step)
#name_new_input = 
