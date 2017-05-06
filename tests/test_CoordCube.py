from rubik_solver import CoordCube
import unittest


class TestCoordCube(unittest.TestCase):
    def test_build_twist_move(self):
        twist_move = CoordCube.build_twist_move()
        self.assertEqual(twist_move, CoordCube.CoordCube.twistMove)

    def test_build_flip_move(self):
        flip_move = CoordCube.build_flip_move()
        self.assertEqual(flip_move, CoordCube.CoordCube.flipMove)

    def test_build_FRtoBR_move(self):
        fr_to_br_move = CoordCube.build_fr_to_br()
        self.assertEqual(fr_to_br_move, CoordCube.CoordCube.FRtoBR_Move)

    def test_build_URFtoDLF_move(self):
        urf_to_dlf_move = CoordCube.build_urf_to_dlf()
        self.assertEqual(urf_to_dlf_move, CoordCube.CoordCube.URFtoDLF_Move)

    def test_build_URtoDF_move(self):
        ur_to_df_move = CoordCube.build_ur_to_df()
        self.assertEqual(ur_to_df_move, CoordCube.CoordCube.URtoDF_Move)

    def test_build_URtoUL_move(self):
        ur_to_ul_move = CoordCube.build_ur_to_ul()
        self.assertEqual(ur_to_ul_move, CoordCube.CoordCube.URtoUL_Move)

    def test_build_UBtoDF_move(self):
        ub_to_df_move = CoordCube.build_ub_to_df()
        self.assertEqual(ub_to_df_move, CoordCube.CoordCube.UBtoDF_Move)

    def test_build_MergeURtoULandUBtoDF(self):
        merge_ur_to_ul_and_ub_to_df = CoordCube.build_merge_ur_to_ul_and_ub_to_df()
        self.assertEqual(merge_ur_to_ul_and_ub_to_df, CoordCube.CoordCube.MergeURtoULandUBtoDF)

    def test_build_Slice_URFtoDLF_Parity_Prun(self):
        slice_urf_to_dlf_parity_prun = CoordCube.build_slice_urf_to_dlf_parity_prun()
        self.assertEqual(slice_urf_to_dlf_parity_prun, CoordCube.CoordCube.Slice_URFtoDLF_Parity_Prun)

    def test_build_Slice_URtoDF_Parity_Prun(self):
        slice_ur_to_df_parity_prun = CoordCube.build_slice_ur_to_df_parity_prun()
        self.assertEqual(slice_ur_to_df_parity_prun, CoordCube.CoordCube.Slice_URtoDF_Parity_Prun)

    def test_build_twist_move(self):
        slice_twist_prun = CoordCube.build_slice_twist_prun()
        self.assertEqual(slice_twist_prun, CoordCube.CoordCube.Slice_Twist_Prun)

