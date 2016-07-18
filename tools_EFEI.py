import numpy as np
from numpy.linalg import norm
import os, re, shutil 
import tools_analysis_efei as tools_usr




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
def parser_lists(data,first,second):
    whole_data = []
    parse = False
    for line in data:
        if str(first) in line:
            parse = True
        elif str(second) in line:
            parse = False
        if parse:
            whole_data.append(line)
    return whole_data



def chunks_optim(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    input_or = [i for i,k in enumerate(lines) if 'Input orientation:' in k]
    chunks = []
    a = 0
    for ind in input_or:
        chunks.append(lines[a:ind])
        a = ind
        if input_or.index(ind) == len(input_or)-1:
            chunks.append(lines[ind:])
        
    b = []
    for geom in chunks:
        for s in geom:
            if 'Normal termination' in s:
             b.append(geom)

    return (b)


def extract_E(filename):
    data = chunks_optim(filename)
    all_E = []
    for i in data:
        a = parser_lists(i,')     EIGENVALUE','Final one electron')
        b = [ k.split() for k in a if 'EIGENVALUE' in k]
        c = map(float,[j[-1] for j in b])
        all_E.append(c)
    return reduce(lambda x,y: x+y,all_E)


def read_geoms(lista_f):
    a = []
    Zs =[]
    for i in lista_f:
        Z = map(str,parsexyz(i)[0])
        for n,z in enumerate(Z):
            if z=='1': Z[n]='H'
            elif z=='7': Z[n]='N'
            elif z=='8': Z[n]='O'
            elif z=='6': Z[n]='C'
        geom_i = parsexyz(i)[1]
        Zs.append(Z)
        a.append(geom_i)
    return zip(a,Zs)

def extract_eners(lista_f):
    eners = [extract_E(filename) for filename in lista_f]
    return eners


def xyz_writer(lista_f,fout):
    Zs_geoms = read_geoms(lista_f)
    Natoms = len(Zs_geoms[0][1])
    with open(fout,'w') as f:
        for geom in Zs_geoms:
            f.write('%s \n' % Natoms)
            f.write('comment \n')
            g = zip(geom[1],geom[0])
            for line in g:
                f.write('%s %s \n' %(line[0], ' '.join(map(str,line[1]))))
    return




def usr_coords(lista_f,arguments):
    geoms = [i[0] for i in read_geoms(lista_f)]
    a = []
    for arg in arguments:
        coords = tools_usr.check_internal(geoms,arg)
        a.append(coords)
    return a


def coords_eners(lista_f,arguments):
    eners = extract_eners(lista_f)
    if len(usr_coords(lista_f,arguments)) > 1:
        coords = zip(*usr_coords(lista_f,arguments))
        return zip(eners,coords)
    else:
        coords = usr_coords(lista_f,arguments)
        coords = zip(*usr_coords(lista_f,arguments))
        return zip(eners,coords)
    

def writer_coords(list_E_coord,fout):
    with open(fout,'w') as f:
        for line in list_E_coord:
            f.write('%s %s \n' %(' '.join(map(str,line[0])), ' '.join(map(str,line[1]))))
    return


def energies_W(filename,filename_ref,atom1,atom2):
    # Mechanical work exerted by the force over two atoms
    return energies_W





def forces_atoms(lista_f,atom1, atom2):
    # Returns total F in atoms


    return modsF






