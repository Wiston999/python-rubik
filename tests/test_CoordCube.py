from rubik_solver import CoordCube
import unittest


class TestCoordCube(unittest.TestCase):
    def _compare_lists(self, l1, l2):
        for i, _ in enumerate(l1):
            self.assertEqual(l1[i], l2[i], msg = "Elements at index %d aren't the same %s != %s" % (
                i, l1[i], l2[i]
            ))

    def _compare_matrices(self, m1, m2):
        for i, _ in enumerate(m1):
            for j, _ in enumerate(m1[i]):
                self.assertEqual(m1[i][j], m2[i][j], msg = "Elements at index [%d][%d] aren't the same %s != %s" % (
                    i, j, m1[i][j], m2[i][j]
                ))

    def test_build_twist_move(self):
        twist_move = CoordCube.build_twist_move()
        self._compare_matrices(twist_move, CoordCube.CoordCube.twistMove)

    def test_build_flip_move(self):
        flip_move = CoordCube.build_flip_move()
        self._compare_matrices(flip_move, CoordCube.CoordCube.flipMove)

    def test_build_FRtoBR_move(self):
        fr_to_br_move = CoordCube.build_fr_to_br()
        self._compare_matrices(fr_to_br_move, CoordCube.CoordCube.FRtoBR_Move)

    def test_build_URFtoDLF_move(self):
        urf_to_dlf_move = CoordCube.build_urf_to_dlf()
        self._compare_matrices(urf_to_dlf_move, CoordCube.CoordCube.URFtoDLF_Move)

    def test_build_URtoDF_move(self):
        ur_to_df_move = CoordCube.build_ur_to_df()
        self._compare_matrices(ur_to_df_move, CoordCube.CoordCube.URtoDF_Move)

    def test_build_URtoUL_move(self):
        ur_to_ul_move = CoordCube.build_ur_to_ul()
        self._compare_matrices(ur_to_ul_move, CoordCube.CoordCube.URtoUL_Move)

    def test_build_UBtoDF_move(self):
        ub_to_df_move = CoordCube.build_ub_to_df()
        self._compare_matrices(ub_to_df_move, CoordCube.CoordCube.UBtoDF_Move)

    def test_build_MergeURtoULandUBtoDF(self):
        merge_ur_to_ul_and_ub_to_df = CoordCube.build_merge_ur_to_ul_and_ub_to_df()
        self._compare_lists(merge_ur_to_ul_and_ub_to_df, CoordCube.CoordCube.MergeURtoULandUBtoDF)

    def test_build_Slice_URFtoDLF_Parity_Prun(self):
        slice_urf_to_dlf_parity_prun = CoordCube.build_slice_urf_to_dlf_parity_prun()
        self._compare_lists(slice_urf_to_dlf_parity_prun, CoordCube.CoordCube.Slice_URFtoDLF_Parity_Prun)

    def test_build_Slice_URtoDF_Parity_Prun(self):
        slice_ur_to_df_parity_prun = CoordCube.build_slice_ur_to_df_parity_prun()
        self._compare_lists(slice_ur_to_df_parity_prun, CoordCube.CoordCube.Slice_URtoDF_Parity_Prun)

    def test_build_twist_prun(self):
        slice_twist_prun = CoordCube.build_slice_twist_prun()
        self._compare_lists(slice_twist_prun, CoordCube.CoordCube.Slice_Twist_Prun)

