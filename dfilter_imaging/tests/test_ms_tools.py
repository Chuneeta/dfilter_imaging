from dfilter_imaging import ms_tools as mt
from dfilter_imaging.data import DATA_PATH
import os
import numpy as np
import nose.tools as nt

msfile = os.path.join(DATA_PATH, 'zen.2458114.31193.HH.xx.t0.ms')

class Test_MSet():
    def test__init__(self):
        ms = mt.MSet(msfile)
        nt.assert_equal(ms.msfile, msfile)

    def test_read_col(self):
        ms = mt.MSet(msfile)
        data = ms.read_col('DATA')
        nt.assert_equal(data.shape, (1, 1024, 51))
        nt.assert_equal(data.dtype, 'complex128')

    def test_transfer_data(self):
        ms = mt.MSet(msfile)
        data = ms.read_col('DATA')   
        ms.transfer_data('DATA', 'MODEL_DATA')
        mod_data = ms.read_col('MODEL_DATA')
        np.testing.assert_almost_equal(data, mod_data)

    def test_get_phase_center(self):
        ms = mt.MSet(msfile)
        pc = ms.get_phase_center()
        nt.assert_equal(pc[0][0][0], 0.8770766867720587)
        nt.assert_equal(pc[1][0][0], -0.5372260675602778)  

    def test_change_phase_center(self):
        ms = mt.MSet(msfile)
        ms.change_phase_center(0, -0.5372260675602778)
        new_pc = ms.get_phase_center()
        nt.assert_equal(new_pc[0][0][0], 0)
        # revert back to normal phase center
        ms.change_phase_center(0.8770766867720587, -0.5372260675602778)
        new_pc = ms.get_phase_center()
        nt.assert_equal(new_pc[0][0][0], 0.8770766867720587)
        nt.assert_equal(new_pc[1][0][0], -0.5372260675602778)
        

    def test_convert_to_uvfits(self):
        ms = mt.MSet(msfile)
        uvfits_name = msfile.replace('.ms', '.uvfits')
        ms.convert_to_uvfits(uvfits_name, overwrite=True)
        nt.assert_true(os.path.exists(uvfits_name))
