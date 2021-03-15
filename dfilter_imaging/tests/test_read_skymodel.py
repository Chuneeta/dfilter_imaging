from dfilter_imaging import read_skymodel as rs
from dfilter_imaging.data import DATA_PATH
import nose.tools as nt
import numpy as np
import os

skymodel = os.path.join(DATA_PATH, 'skymodel.cl')

class Test_Skymodel():
    def __test_init__(self):
        sk = rs.Skymodel(skymodel)
        nt.assert_equal(sk.skymodel, skymodel)

    def test_get_flux_values(self):
        sk = rs.Skymodel(skymodel)
        flux = sk.get_flux_values()
        nt.assert_equal(len(flux), 4)
        nt.assert_equal(flux.dtype, 'complex128')
        np.testing.assert_almost_equal(flux, np.array([[1.+0.j], [0.+0.j],[0.+0.j],[0.+0.j]]))

    def test_get_src_loc(self):
        sk = rs.Skymodel(skymodel)
        src_loc = sk.get_src_loc()
        nt.assert_equal(len(src_loc), 2)
        np.testing.assert_almost_equal(src_loc, np.array([[0.87702795],[0.53721234]]))

    def test_get_sindex(self):
        sk = rs.Skymodel(skymodel)
        sindex = sk.get_sindex()
        nt.assert_equal(len(sindex), 1)
        np.testing.assert_almost_equal(sindex, np.array([[-0.7]]))

    def test_get_freqs(self):
        sk = rs.Skymodel(skymodel)
        freq = sk.get_freqs()
        nt.assert_equal(len(freq), 1)
        np.testing.assert_almost_equal(freq, np.array([1.5e+08]))
        
