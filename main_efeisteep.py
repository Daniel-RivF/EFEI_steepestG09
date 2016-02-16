
import glob, os
import tools_EFEI as tools

first_file = raw_input(' Filename of the g09 first output (for now, im just working with g09 CASSCF gradient calculations)')
atom1 = int(raw_input('First pulling point (atom label)') ) 
atom2 = int(raw_input('Second pulling point (atom label)') )
modF = float(raw_input('Force pair value (for one atom)')
elongation = int(raw_input('Tip 1 for elongation and -1 for compression'))
basename = os.path.splitext(first_file)[0] 
firstname = basename + '000.com'




