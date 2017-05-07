import os

from ..CubieCube import CubieCube

class CoordCube(object):
    '''Representation of the cube on the coordinate level'''
    N_TWIST = 2187 # 3^7 possible corner orientations
    N_FLIP = 2048 # 2^11 possible edge flips
    N_SLICE1 = 495 # 12 choose 4 possible positions of FR,FL,BL,BR edges
    N_SLICE2 = 24 # 4! permutations of FR,FL,BL,BR edges in phase2
    N_PARITY = 2 # 2 possible corner parities
    N_URFtoDLF = 20160 # 8!/(8-6)! permutation of URF,UFL,ULB,UBR,DFR,DLF corners
    N_FRtoBR = 11880 # 12!/(12-4)! permutation of FR,FL,BL,BR edges
    N_URtoUL = 1320 # 12!/(12-3)! permutation of UR,UF,UL edges
    N_UBtoDF = 1320 # 12!/(12-3)! permutation of UB,DR,DF edges
    N_URtoDF = 20160 # 8!/(8-6)! permutation of UR,UF,UL,UB,DR,DF edges in phase2

    N_URFtoDLB = 40320 # 8! permutations of the corners
    N_URtoBR = 479001600 # 8! permutations of the corners

    N_MOVE = 18

    # twistMove = [[0 for _ in range(N_MOVE)] for _ in range( N_TWIST )]	## CUIDADO CON LAS REFERENCIAS
    # flipMove = [[0 for _ in range(N_MOVE)] for _ in range( N_FLIP )]
    # FRtoBR_Move = [[0 for _ in range(N_MOVE)] for _ in range( N_FRtoBR )]
    # URFtoDLF_Move = [[0 for _ in range(N_MOVE)] for _ in range( N_URFtoDLF )]
    # URtoDF_Move = [[0 for _ in range(N_MOVE)] for _ in range( N_URtoDF )]
    # URtoUL_Move = [[0 for _ in range(N_MOVE)] for _ in range( N_URtoUL )]
    # UBtoDF_Move = [[0 for _ in range(N_MOVE)] for _ in range( N_UBtoDF )]
    # MergeURtoULandUBtoDF = [[0 for _ in range(336)] for _ in range( 336 )]

    # Slice_URFtoDLF_Parity_Prun = [-1] * (N_SLICE2 * N_URFtoDLF * N_PARITY // 2)
    # Slice_URtoDF_Parity_Prun = [-1] * (N_SLICE2 * N_URtoDF * N_PARITY // 2)
    # Slice_Twist_Prun = [-1] * (N_SLICE1 * N_TWIST // 2 + 1)
    # Slice_Flip_Prun = [-1] * (N_SLICE1 * N_FLIP // 2)

    ## Parity of the corner permutation. This is the same as the parity for the edge permutation of a valid cube.
    ## parity has values 0 and 1
    parityMove = [
        [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
        [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0]
    ]

    @staticmethod
    def setPruning(table, index, value):
        if (index & 1) == 0:
            table[index // 2] &= (0xf0 | value)
        else:
            table[index // 2] &= (0x0f | (value << 4))

    @staticmethod
    def getPruning(table, index):
        if (index & 1) == 0:
            return table[index // 2] & 0x0f
        else:
            return (table[index // 2] & 0xf0)  >> 4

    def __init__(self, c):
        ''' c is a CubieCube instance'''
        if not isinstance(c, CubieCube):
            raise ValueError('c must be a CubieCube instance, got %s' % c.__class__.__name__)
        self.twist = c.getTwist()
        self.flip = c.getFlip()
        self.parity = c.cornerParity()
        self.FRtoBR = c.getFRtoBR()
        self.URFtoDLF = c.getURFtoDLF()
        self.URtoUL = c.getURtoUL()
        self.UBtoDF = c.getUBtoDF()
        self.URtoDF = c.getURtoDF() # only needed in phase2

    def move(self, m):
        '''A move on the coordinate level'''
        self.twist    = self.twistMove[self.twist][m]
        self.flip     = self.flipMove[self.flip][m]
        self.parity   = self.parityMove[self.parity][m]
        self.FRtoBR   = self.FRtoBR_Move[self.FRtoBR][m]
        self.URFtoDLF = self.URFtoDLF_Move[self.URFtoDLF][m]
        self.URtoUL   = self.URtoUL_Move[self.URtoUL][m]
        self.UBtoDF   = self.UBtoDF_Move[self.UBtoDF][m]
        if self.URtoUL < 336 and self.UBtoDF < 336: #  updated only if UR,UF,UL,UB,DR,DF
            # are not in UD-slice
            self.URtoDF = self.MergeURtoULandUBtoDF[self.URtoUL][self.UBtoDF]

## Init more static values of class CubieCube
def read_or_func_list(file_name, func):
    abspath = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    if os.path.exists(abspath):
        return list(map(int, list(map(str.strip, open(abspath).read().split(',')))))
    else:
        ret = func()
        open(abspath, 'w').write(','.join(str(c) for c in ret))
        return ret

def read_or_func_matrix(file_name, func):
    abspath = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    if os.path.exists(abspath):
        return [list(map(int, list(map(str.strip, l.split(','))))) for l in open(abspath)]
    else:
        ret = func()
        open(abspath, 'w').write('\n'.join(','.join(str(c) for c in l) for l in ret))
        return ret

def build_twist_move():
    twist_move = [[0 for _ in range(CoordCube.N_MOVE)] for _ in range( CoordCube.N_TWIST )]
    a = CubieCube()
    for i in range(CoordCube.N_TWIST):
        a.setTwist(i)
        for j in range(6):
            for k in range(3):
                a.cornerMultiply(CubieCube.moveCube[j])
                twist_move[i][ (3 * j) + k ] = a.getTwist()
            a.cornerMultiply(CubieCube.moveCube[j]) # 4.faceturn restores
    return twist_move

def build_flip_move():
    flip_move = [[0 for _ in range(CoordCube.N_MOVE)] for _ in range( CoordCube.N_FLIP )]
    a = CubieCube()
    for i in range(CoordCube.N_FLIP):
        a.setFlip(i)
        for j in range(6):
            for k in range(3):
                a.edgeMultiply(CubieCube.moveCube[j])
                flip_move[i][ 3 * j + k ] = a.getFlip()
            a.edgeMultiply(CubieCube.moveCube[j])
    return flip_move

def build_urf_to_dlf():
    urf_to_dlf = [[0 for _ in range(CoordCube.N_MOVE)] for _ in range( CoordCube.N_URFtoDLF )]
    a = CubieCube()
    for i in range(CoordCube.N_URFtoDLF):
        a.setURFtoDLF(i)
        for j in range(6):
            for k in range(3):
                a.cornerMultiply(CubieCube.moveCube[j])
                urf_to_dlf[i][ 3 * j + k ] = a.getURFtoDLF()
            a.cornerMultiply(CubieCube.moveCube[j])
    return urf_to_dlf

def build_fr_to_br():
    fr_to_br = [[0 for _ in range(CoordCube.N_MOVE)] for _ in range( CoordCube.N_FRtoBR )]
    a = CubieCube()
    for i in range(CoordCube.N_FRtoBR):
        a.setFRtoBR(i)
        for j in range(6):
            for k in range(3):
                a.edgeMultiply(CubieCube.moveCube[j])
                fr_to_br[i][ 3 * j + k ] = a.getFRtoBR()
            a.edgeMultiply(CubieCube.moveCube[j])
    return fr_to_br

def build_ur_to_df():
    ur_to_df = [[0 for _ in range(CoordCube.N_MOVE)] for _ in range( CoordCube.N_URtoDF )]
    a = CubieCube()
    for i in range(CoordCube.N_URtoDF):
        a.setURtoDF(i)
        for j in range(6):
            for k in range(3):
                a.edgeMultiply(CubieCube.moveCube[j])
                ur_to_df[i][ 3 * j + k ] = a.getURtoDF()
            a.edgeMultiply(CubieCube.moveCube[j])
    return ur_to_df

def build_ur_to_ul():
    ur_to_ul = [[0 for _ in range(CoordCube.N_MOVE)] for _ in range( CoordCube.N_URtoUL )]
    a = CubieCube()
    for i in range(CoordCube.N_URtoUL):
        a.setURtoUL(i)
        for j in range(6):
            for k in range(3):
                a.edgeMultiply(CubieCube.moveCube[j])
                ur_to_ul[i][ 3 * j + k ] = a.getURtoUL()
            a.edgeMultiply(CubieCube.moveCube[j])
    return ur_to_ul

def build_ub_to_df():
    ub_to_df = [[0 for _ in range(CoordCube.N_MOVE)] for _ in range( CoordCube.N_UBtoDF )]
    a = CubieCube()
    for i in range(CoordCube.N_URtoUL):
        a.setUBtoDF(i)
        for j in range(6):
            for k in range(3):
                a.edgeMultiply(CubieCube.moveCube[j])
                ub_to_df[i][ 3 * j + k ] = a.getUBtoDF()
            a.edgeMultiply(CubieCube.moveCube[j])
    return ub_to_df

def build_merge_ur_to_ul_and_ub_to_df():
    merge_ur_to_ul_and_ub_to_df = [[0 for _ in range(336)] for _ in range( 336 )]
    for uRtoUL in range(336):
        for uBtoDF in range(336):
            merge_ur_to_ul_and_ub_to_df[uRtoUL][uBtoDF] = CubieCube.getURtoDFs(uRtoUL, uBtoDF)
    return merge_ur_to_ul_and_ub_to_df

def build_slice_urf_to_dlf_parity_prun():
    slice_urf_to_dlf_parity_prun = [-1] * (CoordCube.N_SLICE2 * CoordCube.N_URFtoDLF * CoordCube.N_PARITY // 2)
    CoordCube.setPruning(slice_urf_to_dlf_parity_prun, 0, 0)
    done, depth = 1, 0
    while done < CoordCube.N_SLICE2 * CoordCube.N_URFtoDLF * CoordCube.N_PARITY:
        for i in range(CoordCube.N_SLICE2 * CoordCube.N_URFtoDLF * CoordCube.N_PARITY):
            parity = i % 2
            URFtoDLF = (i // 2) // CoordCube.N_SLICE2
            slicing = (i // 2) % CoordCube.N_SLICE2
            if CoordCube.getPruning(slice_urf_to_dlf_parity_prun, i) == depth:
                for j in [0, 1, 2, 4, 7, 9, 10, 11, 13, 16]:
                    newSlice = CoordCube.FRtoBR_Move[slicing][j]
                    newURFtoDLF = CoordCube.URFtoDLF_Move[URFtoDLF][j]
                    newParity = CoordCube.parityMove[parity][j]
                    if CoordCube.getPruning(slice_urf_to_dlf_parity_prun, ((CoordCube.N_SLICE2 * newURFtoDLF) + newSlice) * 2 + newParity) == 0x0f:
                        CoordCube.setPruning(slice_urf_to_dlf_parity_prun, ((CoordCube.N_SLICE2 * newURFtoDLF) + newSlice) * 2 + newParity, depth + 1)
                        done += 1

        depth += 1
    return slice_urf_to_dlf_parity_prun

def build_slice_ur_to_df_parity_prun():
    slice_ur_to_df_parity_prun = [-1] * (CoordCube.N_SLICE2 * CoordCube.N_URtoDF * CoordCube.N_PARITY // 2)
    CoordCube.setPruning(slice_ur_to_df_parity_prun, 0, 0)
    done, depth = 1, 0
    while done != (CoordCube.N_SLICE2 * CoordCube.N_URtoDF * CoordCube.N_PARITY):
        for i in range(CoordCube.N_SLICE2 * CoordCube.N_URtoDF * CoordCube.N_PARITY):
            parity = i % 2
            URtoDF = (i // 2) // CoordCube.N_SLICE2
            slicing = (i // 2) % CoordCube.N_SLICE2
            if depth == CoordCube.getPruning(slice_ur_to_df_parity_prun, i):
                for j in [0, 1, 2, 4, 7, 9, 10, 11, 13, 16]:
                    newSlice = CoordCube.FRtoBR_Move[slicing][j]
                    newURtoDF = CoordCube.URtoDF_Move[URtoDF][j]
                    newParity = CoordCube.parityMove[parity][j]
                    if  CoordCube.getPruning(slice_ur_to_df_parity_prun, (CoordCube.N_SLICE2 * newURtoDF + newSlice) * 2 + newParity) == 0x0f:
                        CoordCube.setPruning(slice_ur_to_df_parity_prun, (CoordCube.N_SLICE2 * newURtoDF + newSlice) * 2 + newParity, depth + 1)
                        done += 1
        depth += 1
    return slice_ur_to_df_parity_prun

def build_slice_twist_prun():
    slice_twist_prun = [-1] * (CoordCube.N_SLICE1 * CoordCube.N_TWIST // 2 + 1)
    CoordCube.setPruning(slice_twist_prun, 0, 0)
    done, depth = 1, 0
    while done < (CoordCube.N_SLICE1 * CoordCube.N_TWIST):
        for i in range(CoordCube.N_SLICE1 * CoordCube.N_TWIST):
            twist = i // CoordCube.N_SLICE1
            slicing = i % CoordCube.N_SLICE1
            if CoordCube.getPruning(slice_twist_prun, i) == depth:
                for j in range(18):
                    newSlice = CoordCube.FRtoBR_Move[slicing * 24][j] // 24
                    newTwist = CoordCube.twistMove[twist][j]
                    if CoordCube.getPruning(slice_twist_prun, CoordCube.N_SLICE1 * newTwist + newSlice) == 0x0f:
                        CoordCube.setPruning(slice_twist_prun, CoordCube.N_SLICE1 * newTwist + newSlice, depth + 1)
                        done += 1
        depth += 1
    return slice_twist_prun

def build_slice_flip_prun():
    slice_flip_prun = [-1] * (CoordCube.N_SLICE1 * CoordCube.N_FLIP // 2)
    CoordCube.setPruning(slice_flip_prun, 0, 0)
    done, depth = 1, 0
    while done < (CoordCube.N_SLICE1 * CoordCube.N_FLIP):
        for i in range(CoordCube.N_SLICE1 * CoordCube.N_FLIP):
            flip = i // CoordCube.N_SLICE1
            slicing = i % CoordCube.N_SLICE1
            if CoordCube.getPruning(slice_flip_prun, i) == depth:
                for j in range(18):
                    newSlice = CoordCube.FRtoBR_Move[slicing * 24][j] // 24
                    newFlip = CoordCube.flipMove[flip][j]
                    if CoordCube.getPruning(slice_flip_prun, CoordCube.N_SLICE1 * newFlip + newSlice) == 0x0f:
                        CoordCube.setPruning(slice_flip_prun, CoordCube.N_SLICE1 * newFlip + newSlice, depth + 1)
                        done += 1
        depth += 1
    return slice_flip_prun

CoordCube.twistMove = read_or_func_matrix('twist_move.csv', build_twist_move)

CoordCube.flipMove = read_or_func_matrix('flip_move.csv', build_flip_move)

CoordCube.FRtoBR_Move = read_or_func_matrix('fr_to_br_move.csv', build_fr_to_br)

CoordCube.URFtoDLF_Move = read_or_func_matrix('urf_to_dlf_move.csv', build_urf_to_dlf)

CoordCube.URtoDF_Move = read_or_func_matrix('ur_to_df_move.csv', build_ur_to_df)

CoordCube.URtoUL_Move = read_or_func_matrix('ur_to_ul_move.csv', build_ur_to_ul)

CoordCube.UBtoDF_Move = read_or_func_matrix('ub_to_df_move.csv', build_ub_to_df)

CoordCube.MergeURtoULandUBtoDF = read_or_func_matrix('merge_ur_to_ul_and_ub_to_df_move.csv', build_merge_ur_to_ul_and_ub_to_df)

CoordCube.Slice_URFtoDLF_Parity_Prun = read_or_func_list('slice_urf_to_dlf_parity_prun.csv', build_slice_urf_to_dlf_parity_prun)

CoordCube.Slice_URtoDF_Parity_Prun = read_or_func_list('slice_ur_to_df_parity_prun.csv', build_slice_ur_to_df_parity_prun)

CoordCube.Slice_Twist_Prun = read_or_func_list('slice_twist_prun.csv', build_slice_twist_prun)

CoordCube.Slice_Flip_Prun = read_or_func_list('slice_flip_prun.csv', build_slice_flip_prun)
