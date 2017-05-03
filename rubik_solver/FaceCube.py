from .Enums import Facelet, Color, Edge, Corner
from .CubieCube import CubieCube

class FaceCube(object):
    '''Cube on the facelet level
    Map the corner positions to facelet positions. cornerFacelet[URF.ordinal()][0] e.g. gives the position of the
    facelet in the URF corner position, which defines the orientation.<br>
    cornerFacelet[URF.ordinal()][1] and cornerFacelet[URF.ordinal()][2] give the position of the other two facelets
    '''

    cornerFacelet = [
        [Facelet.U9, Facelet.R1, Facelet.F3],
        [Facelet.U7, Facelet.F1, Facelet.L3],
        [Facelet.U1, Facelet.L1, Facelet.B3],
        [Facelet.U3, Facelet.B1, Facelet.R3],
        [Facelet.D3, Facelet.F9, Facelet.R7],
        [Facelet.D1, Facelet.L9, Facelet.F7],
        [Facelet.D7, Facelet.B9, Facelet.L7],
        [Facelet.D9, Facelet.R9, Facelet.B7]
    ]

    '''Map the edge positions to facelet positions. edgeFacelet[UR.ordinal()][0] e.g. gives the position of the facelet in
    the UR edge position, which defines the orientation.<br>
    edgeFacelet[UR.ordinal()][1] gives the position of the other facelet
    '''
    edgeFacelet = [
        [Facelet.U6, Facelet.R2],
        [Facelet.U8, Facelet.F2],
        [Facelet.U4, Facelet.L2],
        [Facelet.U2, Facelet.B2],
        [Facelet.D6, Facelet.R8],
        [Facelet.D2, Facelet.F8],
        [Facelet.D4, Facelet.L8],
        [Facelet.D8, Facelet.B8],
        [Facelet.F6, Facelet.R4],
        [Facelet.F4, Facelet.L6],
        [Facelet.B6, Facelet.L4],
        [Facelet.B4, Facelet.R6]
    ]

    '''Map the corner positions to facelet colors.'''
    cornerColor = [
        [Color.U, Color.R, Color.F],
        [Color.U, Color.F, Color.L],
        [Color.U, Color.L, Color.B],
        [Color.U, Color.B, Color.R],
        [Color.D, Color.F, Color.R],
        [Color.D, Color.L, Color.F],
        [Color.D, Color.B, Color.L],
        [Color.D, Color.R, Color.B]
    ]

    '''Map the edge positions to facelet colors.'''
    edgeColor = [
        [Color.U, Color.R],
        [Color.U, Color.F],
        [Color.U, Color.L],
        [Color.U, Color.B],
        [Color.D, Color.R],
        [Color.D, Color.F],
        [Color.D, Color.L],
        [Color.D, Color.B],
        [Color.F, Color.R],
        [Color.F, Color.L],
        [Color.B, Color.L],
        [Color.B, Color.R]
    ]

    def __init__(self, cubeString = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"):
        self.f = [0] * 54
        for i in range(54):
            self.f[i] = getattr(Color, cubeString[i])

    def to_String(self):
        '''Gives string representation of a facelet cube'''
        s = ""

        for i in range(54):
            s += Color.reverse_mapping[self.f[i]]
        return s

    def toCubieCube(self):
        '''Gives CubieCube representation of a faceletcube'''
        ccRet = CubieCube()
        for i in range(8):
            ccRet.cp[i] = Corner.URF # invalidate corners
        for i in range(12):
            ccRet.ep[i] = Edge.UR # and edges

        for i in Corner.reverse_mapping.keys():
            # get the colors of the cubie at corner i, starting with U/D
            for ori in range(3):
                if (self.f[FaceCube.cornerFacelet[i][ori]] == Color.U) or (self.f[FaceCube.cornerFacelet[i][ori]] == Color.D):
                    break
            else:
                ori = 3
            col1 = self.f[FaceCube.cornerFacelet[i][(ori + 1) % 3]]
            col2 = self.f[FaceCube.cornerFacelet[i][(ori + 2) % 3]]

            for j in Corner.reverse_mapping.keys():
                if (col1 == FaceCube.cornerColor[j][1]) and (col2 == FaceCube.cornerColor[j][2]):
                    ccRet.cp[i] = j
                    ccRet.co[i] = ori % 3
                    break

        for i in Edge.reverse_mapping.keys():
            for j in Edge.reverse_mapping.keys():
                if (self.f[FaceCube.edgeFacelet[i][0]] == FaceCube.edgeColor[j][0]) and (self.f[FaceCube.edgeFacelet[i][1]] == FaceCube.edgeColor[j][1]):
                    ccRet.ep[i] = j
                    ccRet.eo[i] = 0

                if (self.f[FaceCube.edgeFacelet[i][0]] == FaceCube.edgeColor[j][1]) and (self.f[FaceCube.edgeFacelet[i][1]] == FaceCube.edgeColor[j][0]):
                    ccRet.ep[i] = j
                    ccRet.eo[i] = 1
                    break
        return ccRet

