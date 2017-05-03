__author__ = 'Victor'

import time

from rubik_solver.Enums import Color
import rubik_solver.FaceCube as FaceCube
import rubik_solver.CoordCube as CoordCube
from rubik_solver.CubieCube import DupedEdge


class DupedFacelet(Exception):
    pass


class NoSolution(Exception):
    pass


class SolverTimeoutError(Exception):
    pass

class Search(object):
    ax = [0] * 31  # The axis of the move
    po = [0] * 31  # The power of the move

    flip = [0] * 31  # phase1 coordinates
    twist = [0] * 31
    slice = [0] * 31

    parity = [0] * 31  # phase2 coordinates
    URFtoDLF = [0] * 31
    FRtoBR = [0] * 31
    URtoUL = [0] * 31
    UBtoDF = [0] * 31
    URtoDF = [0] * 31

    minDistPhase1 = [0] * 31  # IDA* distance do goal estimations
    minDistPhase2 = [0] * 31

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # generate the solution string from the array data
    @staticmethod
    def solutionToString(length, depthPhase1=- 1):
        s = []
        for i in range(length):
            step = ''
            if Search.ax[i] == 0:
                step = "U"
            elif Search.ax[i] == 1:
                step = "R"
            elif Search.ax[i] == 2:
                step = "F"
            elif Search.ax[i] == 3:
                step = "D"
            elif Search.ax[i] == 4:
                step = "L"
            elif Search.ax[i] == 5:
                step = "B"

            if Search.po[i] == 2:
                step += "2"
            elif Search.po[i] == 3:
                step += "'"
            if i == (depthPhase1 - 1):
                step = ". "
            s.append(step)
        return s

    @staticmethod
    def solution(facelets, maxDepth, timeOut, useSeparator=False):
        '''
        * Computes the solver string for a given cube.
        *
        * @param facelets
        *          is the cube definition string, see {@link Facelet} for the format.
        *
        * @param maxDepth
        *          defines the maximal allowed maneuver length. For random cubes, a maxDepth of 21 usually will return a
        *          solution in less than 0.5 seconds. With a maxDepth of 20 it takes a few seconds on average to find a
        *          solution, but it may take much longer for specific cubes.
        *
        *@param timeOut
        *          defines the maximum computing time of the method in seconds. If it does not return with a solution, it returns with
        *          an error code.
        *
        * @param useSeparator
        *          determines if a " . " separates the phase1 and phase2 parts of the solver string like in F' R B R L2 F .
        *          U2 U D for example.<br>
        * @return The solution string or an error code:<br>
        *         Error 1: There is not exactly one facelet of each colour<br>
        *         Error 2: Not all 12 edges exist exactly once<br>
        *         Error 3: Flip error: One edge has to be flipped<br>
        *         Error 4: Not all corners exist exactly once<br>
        *         Error 5: Twist error: One corner has to be twisted<br>
        *         Error 6: Parity error: Two corners or two edges have to be exchanged<br>
        *         Error 7: No solution exists for the given maxDepth<br>
        *         Error 8: Timeout, no solution within given time
        '''
        # +++++++++++++++++++++check for wrong input ++++++++++++++++++++++++++
        count = [0] * 6
        try:
            for i in range(54):
                count[getattr(Color, facelets[i])] += 1
        except Exception as e:
            raise DupedFacelet(
                "There is not exactly one facelet of each colour")

        for i in range(6):
            if count[i] != 9:
                raise DupedEdge("Not all 12 edges exist exactly once")

        cc = FaceCube.FaceCube(facelets).toCubieCube()
        try:
            s = cc.verify()
        except Exception as e:
            raise e

        # +++++++++++++++++++++++ initialization ++++++++++++++++++++++++++++++
        c = CoordCube.CoordCube(cc)

        Search.po[0] = 0
        Search.ax[0] = 0
        Search.flip[0] = c.flip
        Search.twist[0] = c.twist
        Search.parity[0] = c.parity
        Search.slice[0] = int(c.FRtoBR) // 24
        Search.URFtoDLF[0] = c.URFtoDLF
        Search.FRtoBR[0] = c.FRtoBR
        Search.URtoUL[0] = c.URtoUL
        Search.UBtoDF[0] = c.UBtoDF

        Search.minDistPhase1[1] = 1  # else failure for depth=1, n=0
        mv, n = 0, 0
        busy = False
        depthPhase1 = 1

        tStart = time.time()

        # +++++++++++++++++++ Main loop +++++++++++++++++++++++++++++++++++++++
        while True:
            while True:
                if (depthPhase1 - n) > Search.minDistPhase1[n + 1] and not busy:
                    if Search.ax[n] == 0 or Search.ax[n] == 3:  # Initialize next move
                        n += 1
                        Search.ax[n] = 1
                    else:
                        n += 1
                        Search.ax[n] = 0
                    Search.po[n] = 1
                else:
                    Search.po[n] += 1
                    if Search.po[n] > 3:
                        while True:
                            Search.ax[n] += 1
                            if Search.ax[n] > 5:
                                if time.time() - tStart > timeOut:
                                    raise SolverTimeoutError(
                                        "Timeout, no solution within given time")

                                if n == 0:
                                    if depthPhase1 >= maxDepth:
                                        raise NoSolution(
                                            "No solution exists for the given maxDepth")
                                    else:
                                        depthPhase1 += 1
                                        Search.ax[n] = 0
                                        Search.po[n] = 1
                                        busy = False
                                        break
                                else:
                                    n -= 1
                                    busy = True
                                    break
                            else:
                                Search.po[n] = 1
                                busy = False

                            if not(n != 0 and (Search.ax[n - 1] == Search.ax[n] or Search.ax[n - 1] - 3 == Search.ax[n])):
                                break
                    else:
                        busy = False
                if not busy:
                    break

            # +++++++++++++ compute new coordinates and new minDistPhase1 +++++
            # if minDistPhase1 =0, the H subgroup is reached
            mv = 3 * Search.ax[n] + Search.po[n] - 1
            Search.flip[n + 1] = CoordCube.CoordCube.flipMove[Search.flip[n]][mv]
            Search.twist[n + 1] = CoordCube.CoordCube.twistMove[Search.twist[n]][mv]
            Search.slice[n + 1] = CoordCube.CoordCube.FRtoBR_Move[Search.slice[n] * 24][mv] // 24
            Search.minDistPhase1[n + 1] = max(
                CoordCube.CoordCube.getPruning(
                    CoordCube.CoordCube.Slice_Flip_Prun, CoordCube.CoordCube.N_SLICE1 * Search.flip[n + 1] + Search.slice[n + 1]),
                CoordCube.CoordCube.getPruning(
                    CoordCube.CoordCube.Slice_Twist_Prun, CoordCube.CoordCube.N_SLICE1 * Search.twist[n + 1] + Search.slice[n + 1])
            )
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

            if Search.minDistPhase1[n + 1] == 0 and n >= (depthPhase1 - 5):
                # instead of 10 any value >5 is possible
                Search.minDistPhase1[n + 1] = 10
                if n == (depthPhase1 - 1):
                    s = Search.totalDepth(depthPhase1, maxDepth)
                    if s >= 0:
                        if s == depthPhase1 or (Search.ax[depthPhase1 - 1] != Search.ax[depthPhase1] and
                          Search.ax[depthPhase1 - 1] != Search.ax[depthPhase1] + 3):
                            return Search.solutionToString(s, depthPhase1 if useSeparator else -1)

    @staticmethod
    def totalDepthPhase2(depthPhase1, depthPhase2, maxDepthPhase2, n):
        busy = False
        while True:
            Search.ax[n] += 1
            if Search.ax[n] > 5:
                if n == depthPhase1:
                    if depthPhase2 >= maxDepthPhase2:
                        return False, busy, n, depthPhase2
                    else:
                        depthPhase2 += 1
                        Search.ax[n] = 0
                        Search.po[n] = 1
                        busy = False
                        break
                else:
                    n -= 1
                    busy = True
                    break
            else:
                if Search.ax[n] == 0 or Search.ax[n] == 3:
                    Search.po[n] = 1
                else:
                    Search.po[n] = 2
                busy = False
            if not (n != depthPhase1 and (Search.ax[n - 1] == Search.ax[n] or (Search.ax[n - 1]) - 3 == Search.ax[n])):
                break
        return True, busy, n, depthPhase2

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Apply phase2 of algorithm and return the combined phase1 and phase2 depth. In phase2, only the moves
    # U,D,R2,F2,L2 and B2 are allowed.
    @staticmethod
    def totalDepth(depthPhase1, maxDepth):
        mv, d1, d2 = 0, 0, 0
        # Allow only max 10 moves in phase2
        maxDepthPhase2 = min(10, maxDepth - depthPhase1)
        for i in range(depthPhase1):
            mv = 3 * Search.ax[i] + Search.po[i] - 1
            Search.URFtoDLF[i + 1] = CoordCube.CoordCube.URFtoDLF_Move[Search.URFtoDLF[i]][mv]
            Search.FRtoBR[i + 1] = CoordCube.CoordCube.FRtoBR_Move[Search.FRtoBR[i]][mv]
            Search.parity[i + 1] = CoordCube.CoordCube.parityMove[Search.parity[i]][mv]

        d1 = CoordCube.CoordCube.getPruning(
            CoordCube.CoordCube.Slice_URFtoDLF_Parity_Prun,
            (CoordCube.CoordCube.N_SLICE2 *
             Search.URFtoDLF[depthPhase1] + Search.FRtoBR[depthPhase1]) * 2 + Search.parity[depthPhase1]
        )
        if d1 > maxDepthPhase2:
            return -1
        for i in range(depthPhase1):
            mv = 3 * Search.ax[i] + Search.po[i] - 1
            Search.URtoUL[i +
                          1] = CoordCube.CoordCube.URtoUL_Move[Search.URtoUL[i]][mv]
            Search.UBtoDF[i +
                          1] = CoordCube.CoordCube.UBtoDF_Move[Search.UBtoDF[i]][mv]

        Search.URtoDF[depthPhase1] = CoordCube.CoordCube.MergeURtoULandUBtoDF[Search.URtoUL[depthPhase1]
                                                                              ][Search.UBtoDF[depthPhase1]]

        d2 = CoordCube.CoordCube.getPruning(
            CoordCube.CoordCube.Slice_URtoDF_Parity_Prun,
            (CoordCube.CoordCube.N_SLICE2 *
             Search.URtoDF[depthPhase1] + Search.FRtoBR[depthPhase1]) * 2 + Search.parity[depthPhase1]
        )
        if d2 > maxDepthPhase2:
            return -1

        Search.minDistPhase2[depthPhase1] = max(d1, d2)
        if Search.minDistPhase2[depthPhase1] == 0:  # already solved
            return depthPhase1

        # now set up search

        depthPhase2 = 1
        n = depthPhase1
        busy = False
        Search.po[depthPhase1] = 0
        Search.ax[depthPhase1] = 0
        Search.minDistPhase2[n + 1] = 1  # else failure for depthPhase2=1, n=0
        # +++++++++++++++++++ end initialization ++++++++++++++++++++++++++++++
        while True:
            while True:
                if (depthPhase1 + depthPhase2 - n) > (Search.minDistPhase2[n + 1]) and not busy:
                    if Search.ax[n] == 0 or Search.ax[n] == 3:  # Initialize next move
                        n += 1
                        Search.ax[n] = 1
                        Search.po[n] = 2
                    else:
                        n += 1
                        Search.ax[n] = 0
                        Search.po[n] = 1
                else:
                    execWhile = False
                    if Search.ax[n] == 0 or Search.ax[n] == 3:
                        Search.po[n] += 1
                        if Search.po[n] > 3:
                            execWhile = True
                    else:
                        Search.po[n] += 2
                        if Search.po[n] > 3:
                            execWhile = True

                    if execWhile:
                        keep_working, busy, n, depthPhase2 = Search.totalDepthPhase2(depthPhase1, depthPhase2, maxDepthPhase2, n)
                        if not keep_working:
                            return -1
                    else:
                        busy = False
                if not busy:
                    break
            # +++++++++++++ compute new coordinates and new minDist ++++++++++
            mv = 3 * Search.ax[n] + Search.po[n] - 1

            Search.URFtoDLF[n +
                            1] = CoordCube.CoordCube.URFtoDLF_Move[Search.URFtoDLF[n]][mv]
            Search.FRtoBR[n +
                          1] = CoordCube.CoordCube.FRtoBR_Move[Search.FRtoBR[n]][mv]
            Search.parity[n +
                          1] = CoordCube.CoordCube.parityMove[Search.parity[n]][mv]
            Search.URtoDF[n +
                          1] = CoordCube.CoordCube.URtoDF_Move[Search.URtoDF[n]][mv]

            Search.minDistPhase2[n + 1] = max(
                CoordCube.CoordCube.getPruning(
                    CoordCube.CoordCube.Slice_URtoDF_Parity_Prun,
                    (CoordCube.CoordCube.N_SLICE2 * Search.URtoDF[n + 1] + Search.FRtoBR[n + 1]) * 2 + Search.parity[n + 1]),
                CoordCube.CoordCube.getPruning(
                    CoordCube.CoordCube.Slice_URFtoDLF_Parity_Prun,
                    (CoordCube.CoordCube.N_SLICE2 *
                     Search.URFtoDLF[n + 1] + Search.FRtoBR[n + 1]) * 2 + Search.parity[n + 1]
                )
            )
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            if Search.minDistPhase2[n + 1] == 0:
                break

        return depthPhase1 + depthPhase2
