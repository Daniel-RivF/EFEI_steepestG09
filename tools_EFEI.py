import numpy as np
from numpy.linalg import norm
import os, re, shutil 

def parseALL(filename,first,second):
    parsing = False
    name = []
    f = open(filename)
    for line in f.readlines():
        if line.startswith(first):
            parsing = True
            continue
        elif line.startswith(second):
            parsing = False
        if parsing:
            a = line.split()
            name.extend(a)
    return name

def Check_termination(filename):
    if 'Normal termination' in open(filename).read():
        return True
    else:
        return False



def parsexyz(filename):
    lst = parseALL(filename," Number     Number       Type","         ")
    lines = map(float,lst[1:-1])
    xyz = [lines[x:x+3] for x in xrange(0, len(lines), 3)] 
    b = xyz[1::2]
    Z = map(int,lines[1::6])
    return (Z,np.array(b)) 


def read_force(filename):
    lst = parseALL(filename,' Center     Atomic                   Forces',' Cartesian Forces:')
    lines = map(float,lst[6:-1]) 
    f = [lines[x:x+5] for x in  xrange(0,len(lines),5)]
    fmat = np.array([i[2:] for i in f])
    return fmat



def construct_fvector(filename,atom1,atom2,modF,elongation):
    xyz = parsexyz(filename)[1]
    N = len(xyz)
    u2 = (xyz[atom2-1]-xyz[atom1-1]) / norm(xyz[atom2-1]-xyz[atom1-1])
    if elongation == 1:
        f2 = u2 * modF / 82.387
        f1 = -f2
        z = np.zeros((N,3))
        z[atom2-1] = f2
        z[atom1-1] = f1
        return z
    elif elongation == -1:
        f1 = u2 * modF / 82.387
        f2 = -f1
        z = np.zeros((N,3))
        z[atom1-1] = f1
        z[atom2-1] = f2
        return z


def new_xyzvector(filename,fvector,step):
    # fvector from construct_fvector.
    f_prev = read_force(filename)
    f_new = f_prev + fvector
    old_xyz = parsexyz(filename)[1]
    new_xyz = old_xyz + step * f_new
    return new_xyz

def new_input(file_inp,route_sect,charge,spin,Z,new_xyz):
    xyz = zip(Z,new_xyz.tolist())
    chk = os.path.splitext(file_inp)[0]
    chk1 = re.sub('[._-]', '', chk)
    with open(file_inp,'w') as f:
         f.write('%schk=%s \n' %('%',chk1 + '.chk'))
         f.write('%nproc=4 \n')
         f.write('%mem=4gb \n')
         f.write('%s \n' % route_sect)
         f.write(' \n')
         f.write('COMMENT \n')
         f.write(' \n')
         f.write('%s %s \n' %(charge,spin))
         for line in xyz:
             f.write('%s %s \n' %(line[0], ' '.join(map(str,line[1]))))
         f.write('  \n')
    return



#
#    with open(filename,'w') as f:
#        f.write('%chk = %s ' % )
#
#
#    return


##########################################
############## Analyze results ###########
##########################################

def forces_atoms(files,atoms):

    return modsF

def xyz_geoms(files):

    return





