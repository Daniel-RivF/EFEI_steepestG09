import numpy as np
from numpy.linalg import norm

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


def parsexyz(filename):
    lst = parseALL(filename," Number     Number       Type","         ")
    lines = map(float,lst[1:-1])
    xyz = [lines[x:x+3] for x in xrange(0, len(lines), 3)] 
    b = xyz[1::2]
    Z = map(int,lines[1::6])
    return (Z,np.array(b)) 


def read_force(filename):
    lst = parseALL(filename,'Center     Atomic                   Forces','Cartesian Forces:')
    lines = map(float,lst[6:-1]) 
    f = [lines[x:x+3] for x in  xrange(0,len(lines),3)]
    fmat = np.array([i[2:] for i in a])
    return fmat



def construct_fvector(filename,atom1,atom2,modF,elongation):
    xyz = parsexyz(filename)
    N = len(xyz)
    u2 = (xyz[atom2-1]-xyz[atom1-1]) / norm(xyz[atom2-1]-xyz[atom1-1])
    if elongation == 1:
        f2 = u2 * modF
        f1 = -f2
        z = np.zeros((N,3))
        z[atom2-1] = f2
        z[atom1-1] = f1
        return z
    elif elongation == -1:
        f1 = u2 * modF
        f2 = -f1
        z = np.zeros((N,3))
        z[atom1-1] = f1
        z[atom2-1] = f2
        return z

def new_xyz(xyz_prev,fvector_prev,step):
    #Steepest (Force direction)
    n_xyz = xyz_prev + step * fvector_prev

    return new_xyz


def new_input(charge,spin,xyz,name):

    return


##########################################
############## Analyze results ###########
##########################################

def forces_atoms(files,atoms):

    return modsF

def xyz_geoms(files):

    return





