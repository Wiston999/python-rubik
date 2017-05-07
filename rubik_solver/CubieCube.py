from .Enums import Corner, Edge

class DupedEdge(Exception): pass
class FlipError(Exception): pass
class DupedCorner(Exception): pass
class TwistError(Exception): pass
class ParityError(Exception): pass

class CubieCube(object):
    '''Cube on the cubie level'''

    ## moves on the cubie level
    cpU = [
        Corner.UBR, Corner.URF, Corner.UFL, Corner.ULB, Corner.DFR, Corner.DLF, Corner.DBL, Corner.DRB
    ]
    coU = [0] * 8
    epU = [
        Edge.UB, Edge.UR, Edge.UF, Edge.UL, Edge.DR, Edge.DF, Edge.DL, Edge.DB, Edge.FR, Edge.FL, Edge.BL, Edge.BR
    ]
    eoU = [0] * 12

    cpR = [
        Corner.DFR, Corner.UFL, Corner.ULB, Corner.URF, Corner.DRB, Corner.DLF, Corner.DBL, Corner.UBR
    ]
    coR =  [2, 0, 0, 1, 1, 0, 0, 2]
    epR = [
        Edge.FR, Edge.UF, Edge.UL, Edge.UB, Edge.BR, Edge.DF, Edge.DL, Edge.DB, Edge.DR, Edge.FL, Edge.BL, Edge.UR
    ]
    eoR = [0] * 12

    cpF = [
        Corner.UFL, Corner.DLF, Corner.ULB, Corner.UBR, Corner.URF, Corner.DFR, Corner.DBL, Corner.DRB
    ]
    coF =  [1, 2, 0, 0, 2, 1, 0, 0]
    epF = [
        Edge.UR, Edge.FL, Edge.UL, Edge.UB, Edge.DR, Edge.FR, Edge.DL, Edge.DB, Edge.UF, Edge.DF, Edge.BL, Edge.BR
    ]
    eoF = [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0]

    cpD = [
        Corner.URF, Corner.UFL, Corner.ULB, Corner.UBR, Corner.DLF, Corner.DBL, Corner.DRB, Corner.DFR
    ]
    coD =  [0] * 8
    epD = [
        Edge.UR, Edge.UF, Edge.UL, Edge.UB, Edge.DF, Edge.DL, Edge.DB, Edge.DR, Edge.FR, Edge.FL, Edge.BL, Edge.BR
    ]
    eoD = [0] * 12

    cpL = [
        Corner.URF, Corner.ULB, Corner.DBL, Corner.UBR, Corner.DFR, Corner.UFL, Corner.DLF, Corner.DRB
    ]
    coL =  [0, 1, 2, 0, 0, 2, 1, 0]
    epL = [
        Edge.UR, Edge.UF, Edge.BL, Edge.UB, Edge.DR, Edge.DF, Edge.FL, Edge.DB, Edge.FR, Edge.UL, Edge.DL, Edge.BR
    ]
    eoL = [0] * 12

    cpB = [
        Corner.URF, Corner.UFL, Corner.UBR, Corner.DRB, Corner.DFR, Corner.DLF, Corner.ULB, Corner.DBL
    ]
    coB =  [0, 0, 1, 2, 0, 0, 2, 1]
    epB = [
        Edge.UR, Edge.UF, Edge.UL, Edge.BR, Edge.DR, Edge.DF, Edge.DL, Edge.BL, Edge.FR, Edge.FL, Edge.UB, Edge.DB
    ]
    eoB = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1]

    def __init__(self, cp = None, co = None, ep = None, eo = None):

        if cp is None or co is None or ep is None or eo is None:
            ## corner permutation
            cp = [
                Corner.URF, Corner.UFL, Corner.ULB, Corner.UBR, Corner.DFR, Corner.DLF, Corner.DBL, Corner.DRB
            ]

            ## corner orientation
            co = [0] * 8

            ## edge permutation
            ep = [
                Edge.UR, Edge.UF, Edge.UL, Edge.UB, Edge.DR, Edge.DF, Edge.DL, Edge.DB, Edge.FR, Edge.FL, Edge.BL, Edge.BR
            ]

            ## edge orientation
            eo = [0] * 12

        self.cp = cp
        self.co = co

        self.ep = ep
        self.eo = eo

    @staticmethod
    def Cnk(n, k):
        '''n choose k'''
        if n < k:
            return 0
        if k > (n // 2):
            k = n - k
        s, i, j = 1, n, 1
        while i != (n - k):
            s *= i
            s //= j

            i -= 1
            j += 1

        return s

    @staticmethod
    def rotateLeft(arr, l, r):
        '''Left rotation of all array elements between l and r'''
        tmp = arr[l]
        for i in range(l, r):
            arr[i] = arr[i + 1]
        arr[r] = tmp

    @staticmethod
    def rotateRight(arr, l, r):
        '''Right rotation of all array elements between l and r'''
        tmp = arr[r]
        for i in range(r, l, -1):
            arr[i] = arr[i - 1]
        arr[l] = tmp

    def cornerMultiply(self, b):
        ''' Multiply this CubieCube with another cubiecube b, restricted to the corners.<br>
            Because we also describe reflections of the whole cube by permutations, we get a complication with the corners. The
            orientations of mirrored corners are described by the numbers 3, 4 and 5. The composition of the orientations
            cannot be computed by addition modulo three in the cyclic group C3 any more. Instead the rules below give an addition in
            the dihedral group D3 with 6 elements.
            
            NOTE: Because we do not use symmetry reductions and hence no mirrored cubes in this simple implementation of the
            Two-Phase-Algorithm, some code is not necessary here.
        '''
        cPerm = [0] * 8
        cOri = [0] * 8

        for corn in Corner.reverse_mapping.keys():
            cPerm[corn] = self.cp[b.cp[corn]]

            oriA = self.co[b.cp[corn]]
            oriB = b.co[corn]
            ori = 0
            if (oriA < 3) and (oriB < 3): #if both cubes are regular cubes...
                ori = oriA + oriB #	just do an addition modulo 3 here
                if ori >= 3:
                    ori -= 3
            elif (oriA < 3) and (oriB >= 3): # if cube b is in a mirrored
                ori = oriA - oriB
                if ori < 3:
                    ori += 3
            elif (oriA >= 3) and (oriB >= 3): # if both cubes are in mirrored
                ori = oriA - oriB
                if ori < 0:
                    ori += 3
            cOri[corn] = ori

        self.cp = cPerm
        self.co = cOri

    def edgeMultiply(self, b):
        '''Multiply this CubieCube with another cubiecube b, restricted to the edges.'''
        ePerm = [0] * 12
        eOri = [0] * 12

        for edge in Edge.reverse_mapping.keys():
            ePerm[edge] = self.ep[b.ep[edge]]
            eOri[edge] = (b.eo[edge] + self.eo[b.ep[edge]]) % 2

        self.ep = ePerm
        self.eo = eOri

    def multiply(self, b):
        '''Multiply this CubieCube with another CubieCube b.'''
        self.cornerMultiply(b)

    def invCubieCube(self, c):
        '''Compute the inverse CubieCube'''
        for edge in Edge.reverse_mapping.keys():
            c.ep[self.ep[edge]] = edge
        for edge in Edge.reverse_mapping.keys():
            c.eo[edge] = self.eo[c.ep[edge]]
        for corn in Corner.reverse_mapping.keys():
            c.cp[self.cp[corn]] = corn
        for corn in Corner.reverse_mapping.keys():
            ori = self.co[c.cp[corn]]
            if ori >= 3:
                c.co[corn] = ori
            else:
                c.co[corn] = -ori
                if c.co[corn] < 0:
                    c.co[corn] += 3

    def getTwist(self):
        '''return the twist of the 8 corners. 0 <= twist < 3^7'''
        ret = 0
        for i in range(Corner.URF, Corner.DRB):
            ret = (3 * ret) + self.co[i]

        return ret

    def setTwist(self, twist):
        twistParity = 0
        for i in range(Corner.DRB - 1, Corner.URF - 1, -1):
            self.co[i] = (twist % 3)
            twistParity += self.co[i]
            twist //= 3
        self.co[Corner.DRB] = (3 - (twistParity % 3)) % 3

    def getFlip(self):
        '''return the flip of the 12 edges. 0 <= flip < 2^11'''
        ret = 0
        for i in range(Edge.UR, Edge.BR):
            ret = (2 * ret) + self.eo[i]

        return ret

    def setFlip(self, flip):
        flipParity = 0
        for i in range(Edge.BR - 1, Edge.UR - 1, -1):
            self.eo[i] = (flip % 2)
            flipParity += self.eo[i]
            flip //= 2
        self.eo[Edge.BR] = (2 - (flipParity % 2)) % 2

    def cornerParity(self):
        '''Parity of the corner permutation'''
        s = 0
        for i in range(Corner.DRB, Corner.URF, -1):
            for j in range(i - 1, Corner.URF - 1, -1):
                if self.cp[j] > self.cp[i]:
                    s += 1
        return s % 2

    def edgeParity(self):
        '''Parity of the edges permutation. Parity of corners and edges are the same if the cube is solvable.'''
        s = 0
        for i in range(Edge.BR, Edge.UR, -1):
            for j in range(i - 1, Edge.UR - 1, -1):
                if self.ep[j] > self.ep[i]:
                    s += 1
        return s % 2

    def getFRtoBR(self):
        '''permutation of the UD-slice edges FR,FL,BL and BR'''
        a, x = 0, 0
        edge4 = [0] * 4
        for j in range(Edge.BR, Edge.UR - 1, -1):
            if (Edge.FR <= self.ep[j]) and (self.ep[j] <= Edge.BR):
                a += CubieCube.Cnk(11 - j, x + 1)
                edge4[3 - x] = self.ep[j]
                x += 1

        b = 0
        for j in [3, 2, 1]:
            k = 0
            while edge4[j] != (j + 8):
                CubieCube.rotateLeft(edge4, 0, j)
                k += 1
            b = ((j + 1) * b) + k

        return (24 * a) + b

    def setFRtoBR(self, idx):
        x = 0
        sliceEdge = [Edge.FR, Edge.FL, Edge.BL, Edge.BR]
        otherEdge = [Edge.UR, Edge.UF, Edge.UL, Edge.UB, Edge.DR, Edge.DF, Edge.DL, Edge.DB]
        b = idx % 24
        a = idx // 24

        for e in Edge.reverse_mapping.keys():
            self.ep[e] = Edge.DB

        for j in [1, 2, 3]:
            k = b % (j + 1)
            b //= j + 1
            while k > 0:
                CubieCube.rotateRight(sliceEdge, 0, j)
                k -= 1
        x = 3
        for j in range(Edge.UR, Edge.BR + 1):
            if (a - CubieCube.Cnk(11 - j, x + 1)) >= 0:
                self.ep[j] = sliceEdge[3 - x]
                a -= CubieCube.Cnk(11 - j, x + 1)
                x -= 1

        x = 0
        for j in range(Edge.UR, Edge.BR + 1):
            if self.ep[j] == Edge.DB:
                self.ep[j] = otherEdge[x]
                x += 1

    def getURFtoDLF(self):
        '''Permutation of all corners except DBL and DRB'''
        a, x = 0, 0
        corner6 = [0] * 6
        for j in range(Corner.URF, Corner.DRB + 1):
            if self.cp[j] <= Corner.DLF:
                a += CubieCube.Cnk(j, x + 1)
                corner6[x] = self.cp[j]
                x += 1

        b = 0
        for j in [5, 4, 3, 2, 1]:
            k = 0
            while corner6[j] != j:
                CubieCube.rotateLeft(corner6, 0, j)
                k += 1
            b = (j + 1) * b + k
        return 720 * a + b

    def setURFtoDLF(self, idx):
        corner6 = [Corner.URF, Corner.UFL, Corner.ULB, Corner.UBR, Corner.DFR, Corner.DLF]
        otherCorner = [Corner.DBL, Corner.DRB]
        b = idx % 720
        a = idx // 720

        for c in Corner.reverse_mapping.keys():
            self.cp[c] = Corner.DRB

        for j in [1, 2, 3, 4, 5]:
            k = b % (j + 1)
            b //= j + 1
            while k > 0:
                k -= 1
                CubieCube.rotateRight(corner6, 0, j)

        x = 5
        for j in range(Corner.DRB, -1, -1):
            if (a - CubieCube.Cnk(j, x + 1)) >= 0:
                self.cp[j] = corner6[x]
                a -= CubieCube.Cnk(j, x + 1)
                x -= 1
        x = 0
        for j in range(Corner.URF, Corner.DRB + 1):
            if self.cp[j] == Corner.DRB:
                self.cp[j] = otherCorner[x]
                x += 1

    def getURtoDF(self):
        '''Permutation of the six edges UR,UF,UL,UB,DR,DF.'''
        a, b, x = 0, 0, 0
        edge6 = [0] * 6
        for j in range(Edge.UR, Edge.BR + 1):
            if self.ep[j] <= Edge.DF:
                a += CubieCube.Cnk(j, x + 1)
                edge6[x] = self.ep[j]
                x += 1

        for j in [5, 4, 3, 2, 1]: # compute the index b < 6! for the
            k = 0
            while edge6[j] != j:
                CubieCube.rotateLeft(edge6, 0, j)
                k += 1
            b = (j + 1) * b + k
        return 720 * a + b

    def setURtoDF(self, idx):
        edge6 = [Edge.UR, Edge.UF, Edge.UL, Edge.UB, Edge.DR, Edge.DF]
        otherEdge = [Edge.DL, Edge.DB, Edge.FR, Edge.FL, Edge.BL, Edge.BR]
        b = idx % 720 # Permutation
        a = idx // 720 # Combination
        for e in Edge.reverse_mapping.keys():
            self.ep[e] = Edge.BR # Use BR to invalidate all edges

        for j in [1, 2, 3, 4, 5]:
            k = b % (j + 1)
            b //= j + 1
            while k > 0:
                k -= 1
                CubieCube.rotateRight(edge6, 0, j)
        x = 5
        for j in range(Edge.BR, -1, -1):
            if (a - CubieCube.Cnk(j, x + 1)) >= 0:
                self.ep[j] = edge6[x]
                a -= CubieCube.Cnk(j, x + 1)
                x -= 1

        x = 0
        for j in range(Edge.UR, Edge.BR + 1):
            if self.ep[j] == Edge.BR:
                self.ep[j] = otherEdge[x]
                x += 1

    @staticmethod
    def getURtoDFs(idx1, idx2):
        '''Permutation of the six edges UR,UF,UL,UB,DR,DF'''
        a = CubieCube()
        b = CubieCube()
        a.setURtoUL(idx1)
        b.setUBtoDF(idx2)
        for i in range(8):
            if a.ep[i] != Edge.BR:
                if b.ep[i] != Edge.BR: # collision
                    return -1
                else:
                    b.ep[i] = a.ep[i]
        return b.getURtoDF()

    def getURtoUL(self):
        '''Permutation of the three edges UR,UF,UL'''
        x, a, = 0, 0
        edge3 = [0] * 3
        # compute the index a < (12 choose 3) and the edge permutation.
        for j in range(Edge.UR, Edge.BR + 1):
            if self.ep[j] <= Edge.UL:
                a += CubieCube.Cnk(j, x + 1)
                edge3[x] = self.ep[j]
                x += 1

        b = 0
        for j in [2, 1]: # compute the index b < 3! for the permutation in edge3
            k = 0
            while edge3[j] != j:
                CubieCube.rotateLeft(edge3, 0, j)
                k += 1

            b = (j + 1) * b + k
        return 6 * a + b

    def setURtoUL(self, idx):
        edge3 = [Edge.UR, Edge.UF, Edge.UL]
        b = idx % 6 # Permutation
        a = idx // 6 # Combination
        for e in Edge.reverse_mapping.keys():
            self.ep[e] = Edge.BR # Use BR to invalidate all edges

        for j in [1, 2]: # generate permutation from index b
            k = b % (j + 1)
            b //= j + 1
            while k > 0:
                CubieCube.rotateRight(edge3, 0, j)
                k -= 1

        x = 2 # generate combination and set edges
        for j in range(Edge.BR, -1, -1):
            if (a - CubieCube.Cnk(j, x + 1)) >= 0:
                self.ep[j] = edge3[x]
                a -= CubieCube.Cnk(j, x + 1)
                x -= 1

    def getUBtoDF(self):
        a, x = 0, 0
        edge3 = [0] * 3
        # compute the index a < (12 choose 3) and the edge permutation.
        for j in range(Edge.UR, Edge.BR + 1):
            if Edge.UB <= self.ep[j] and self.ep[j] <= Edge.DF:
                a += CubieCube.Cnk(j, x + 1)
                edge3[x] = self.ep[j]
                x += 1

        b = 0
        for j in [2, 1]: #compute the index b < 3! for the permutation in edge3
            k = 0
            while edge3[j] != (Edge.UB + j):
                CubieCube.rotateLeft(edge3, 0, j)
                k += 1

            b = (j + 1) * b + k

        return 6 * a + b

    def setUBtoDF(self, idx):
        edge3 = [Edge.UB, Edge.DR, Edge.DF]
        b = idx % 6 # Permutation
        a = idx // 6 # Combination
        for e in Edge.reverse_mapping.keys():
            self.ep[e] = Edge.BR # Use BR to invalidate all edges

        for j in [1, 2]: #generate permutation from index b
            k = b % (j + 1)
            b //= j + 1
            while k > 0:
                k-=1
                CubieCube.rotateRight(edge3, 0, j)

        x = 2 # generate combination and set edges
        for j in range(Edge.BR, -1, -1):
            if (a - CubieCube.Cnk(j, x + 1)) >= 0:
                self.ep[j] = edge3[x]
                a -= CubieCube.Cnk(j, x + 1)
                x -= 1

    def getURFtoDLB(self):
        perm = [0] * 8
        b = 0
        for i in range(8):
            perm[i] = self.cp[i]

        for j in range(7, 0, -1): #compute the index b < 8! for the permutation in perm
            k = 0
            while perm[j] != j:
                CubieCube.rotateLeft(perm, 0, j)
                k += 1
            b = (j + 1) * b + k

        return b

    def setURFtoDLB(self, idx):
        perm = [ Corner.URF, Corner.UFL, Corner.ULB, Corner.UBR, Corner.DFR, Corner.DLF, Corner.DBL, Corner.DRB ]
        for j in range(1, 8):
            k = idx % (j + 1)
            idx //= j + 1
            while k > 0:
                k -= 1
                CubieCube.rotateRight(perm, 0, j)

        x = 7 # set corners
        for j in range(7, -1, -1):
            self.cp[j] = perm[x]
            x -= 1

    def getURtoBR(self):
        perm = [0] * 12
        b = 0
        for i in range(12):
            perm[i] = self.ep[i]
        for j in range(11, 0, -1): # compute the index b < 12! for the permutation in perm
            k = 0
            while perm[j] != j:
                CubieCube.rotateLeft(perm, 0, j)
                k += 1

            b = (j + 1) * b + k
        return b

    def setURtoBR(self, idx):
        perm = [ Edge.UR, Edge.UF, Edge.UL, Edge.UB, Edge.DR, Edge.DF, Edge.DL, Edge.DB, Edge.FR, Edge.FL, Edge.BL, Edge.BR ]
        for j in range(1, 12):
            k = idx % (j + 1)
            idx //= j + 1
            while k > 0:
                k -= 1
                CubieCube.rotateRight(perm, 0, j)

        x = 11 # set edges
        for j in range(11, -1, -1):
            self.ep[j] = perm[x]
            x -= 1

    def verify(self):
        '''
        Check a cubiecube for solvability. Return the error code.
        0: Cube is solvable
        -2: Not all 12 edges exist exactly once
        -3: Flip error: One edge has to be flipped
        -4: Not all corners exist exactly once
        -5: Twist error: One corner has to be twisted
        -6: Parity error: Two corners or two edges have to be exchanged
        '''
        suma = 0
        edgeCount = [0] * 12
        for e in Edge.reverse_mapping.keys():
            edgeCount[self.ep[e]] += 1
        for i in range(12):
            if edgeCount[i] != 1:
                raise DupedEdge("Not all 12 edges exist exactly once")

        for i in range(12):
            suma += self.eo[i]
        if suma % 2 != 0:
            raise FlipError("One edge has to be flipped")

        cornerCount = [0] * 8
        for c in Corner.reverse_mapping.keys():
            cornerCount[self.cp[c]] += 1
        for i in range(8):
            if cornerCount[i] != 1:
                raise DupedCorner("Not all corners exist exactly once")

        suma = 0
        for i in range(8):
            suma += self.co[i]
        if suma % 3 != 0:
            raise TwistError("One corner has to be twisted")

        if (self.edgeParity() ^ self.cornerParity()) != 0:
            raise ParityError("Two corners or two edges have to be exchanged")

        return True

## Init more static values of class CubieCube
CubieCube.moveCube = [CubieCube() for _ in range(6)]
CubieCube.moveCube[0].cp = CubieCube.cpU[:]
CubieCube.moveCube[0].co = CubieCube.coU[:]
CubieCube.moveCube[0].ep = CubieCube.epU[:]
CubieCube.moveCube[0].eo = CubieCube.eoU[:]

CubieCube.moveCube[1].cp = CubieCube.cpR[:]
CubieCube.moveCube[1].co = CubieCube.coR[:]
CubieCube.moveCube[1].ep = CubieCube.epR[:]
CubieCube.moveCube[1].eo = CubieCube.eoR[:]

CubieCube.moveCube[2].cp = CubieCube.cpF[:]
CubieCube.moveCube[2].co = CubieCube.coF[:]
CubieCube.moveCube[2].ep = CubieCube.epF[:]
CubieCube.moveCube[2].eo = CubieCube.eoF[:]

CubieCube.moveCube[3].cp = CubieCube.cpD[:]
CubieCube.moveCube[3].co = CubieCube.coD[:]
CubieCube.moveCube[3].ep = CubieCube.epD[:]
CubieCube.moveCube[3].eo = CubieCube.eoD[:]

CubieCube.moveCube[4].cp = CubieCube.cpL[:]
CubieCube.moveCube[4].co = CubieCube.coL[:]
CubieCube.moveCube[4].ep = CubieCube.epL[:]
CubieCube.moveCube[4].eo = CubieCube.eoL[:]

CubieCube.moveCube[5].cp = CubieCube.cpB[:]
CubieCube.moveCube[5].co = CubieCube.coB[:]
CubieCube.moveCube[5].ep = CubieCube.epB[:]
CubieCube.moveCube[5].eo = CubieCube.eoB[:]
