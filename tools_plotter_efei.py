import numpy as np
from numpy.linalg import norm
import os, re, shutil, math 


###
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

    #a=sorted(glob.glob('*/*.log')) , [parsexyz(filename) for filename in a]

def check_internal(geoms,argument):
    class ErrorArgument(Exception): pass
    #Takes a list as argument and checks its length ( 2 for distance, 3 for angles, 4 for dihedrals)
    if all(isinstance(item,int) for item in argument):
        if len(argument) == 2:
            i,j = argument[0],argument[1]
            d = get_Distance(geoms,i,j)
            return d
        elif len(argument) == 3:
            i,j,k = argument[0],argument[1],argument[2]
            angles = get_angles(geoms, i,j,k)
            return angles
        elif len(argument) == 4:
            i,j,k,l = argument[0],argument[1],argument[2],argument[3]
            dihs = get_dihedrals(geoms,i,j,k,l)
            return dihs
        elif   len(argument) >= 5 or len(argument) == 0:
            raise ErrorArgument('Error, list must have less than five elements')
    raise ErrorArgument('List must contain the indexes of atoms i.e. [1,2] for the distance between atoms 1 and 2')

###################### Forces stuff #####################

def read_force(filename):
    lst = parseALL(filename,' Center     Atomic                   Forces',' Cartesian Forces:')
    lines = map(float,lst[6:-1]) 
    f = [lines[x:x+5] for x in  xrange(0,len(lines),5)]
    fmat = np.array([i[2:] for i in f])
    return fmat

def forces_atom(forces,argument):
    """forces=[read_force(filename) for filename in a]"""
    to_nN = 82.387
    if len(argument) == 2:
        atom1 = argument[0]
        atom2 = argument[1]
        forces_atoms = zip([ norm(i[atom1-1])*to_nN for i in forces],[norm(i[atom2-1])*to_nN for i in forces])
        return forces_atoms
    else:
        return "not a distance"

def get_mechanicalW(list_xyz,modF,atom1,atom2):
    """ Gets mechanical work: takes as reference coordinate value at the first point """
    distances = get_Distance(list_xyz, atom1, atom2)
    ref 
    return list_W



##########################################
############## Analyze results ###########
##########################################

def forces_atoms(files,atoms):

    return modsF


################ Internals math functions ##############3

def unit_vect(v):
    return v / norm(v)


def get_Distance(geoms, index1, index2):
    geom_matrix = geoms
    dists = []
    for g in geom_matrix:
        dist = norm(g[index2-1] - g[index1-1])
        dists.append(dist)
    return dists

def angle(v1,v2):
    v1u = unit_vect(v1)
    v2u = unit_vect(v2)
    #angle = np.arccos(np.dot(v1u, v2u))
    angle = math.acos(np.dot(v1u, v2u))
    if np.isnan(angle):
       if (v1u == v2u).all():
           return 0.0 
       else:
           return np.pi
    return angle

def get_angles(geoms, index1,index2,index3):
    coords = geoms
    angles = []
    for ge in coords:
        v12 =  ge[index1 -1] - ge[index2-1] 
        v32 = ge[index3-1] -ge[index2 - 1]
        ang = angle(v12,v32)
        angles.append(ang)
    angles_deg = [ i*(180/np.pi) for i in angles]
    return angles_deg


def dihedral(v21,v32,v43):
    normal1u = unit_vect(np.cross(v21,v32))
    normal2u = unit_vect(np.cross(v32,v43))
    v32n = unit_vect(v32)
    m1 = np.cross(normal1u,v32n)
    x = np.dot(normal1u,normal2u)
    y = np.dot(m1,normal2u)
    torsion = math.atan2(y,x) * 180 / math.pi
    return torsion

def correction_dihedrals(uncorr_dih_list):
    ref0 = uncorr_dih_list[0]
    ref = uncorr_dih_list[0]
    if ref > 0:
        ref = ref - 360
        ref0 = ref0 - 360
    dlist = []
    for d in uncorr_dih_list[1:]:
        if d > 0:
            p = d - 360
        elif d < 0:
            p = d + 360
        wa = d - ref
        wb = p - ref
        if math.fabs(wa) <= math.fabs(wb):
            dihed = d
        else:
            dihed = p
        dlist.append(dihed)
        ref = dihed
    return [ref0] + dlist

def get_dihedrals(geoms, i1, i2, i3, i4):
    # Returns dihedral angles in degrees, corrected 
    coords = geoms
    dihedrals_deg = []
    for ge in coords:
        v21 = ge[i2 -1] - ge[i1-1]
        v32 = ge[i3-1] - ge[i2-1]
        v43 = ge[i4-1] - ge[i3-1]
        dih = dihedral(v21,v32,v43)
        dihedrals_deg.append(dih)
    corr_dihs = correction_dihedrals(dihedrals_deg)
    return corr_dihs

def transform2array(geoms):
    o = []
    for geom in geoms:
        n = [map(float,j[1:]) for j in geom]
        o.append(n)
    geom_matrix = [ np.array(i) for i in o ] 
    return geom_matrix








