from dfilter_imaging import simulate as sm
from dfilter_imaging import read_skymodel as rs
from dfilter_imaging.data import DATA_PATH 
import nose.tools as nt
import numpy as np
import os

# MSFILE
msfile = os.path.join(DATA_PATH, 'zen.2458114.31193.HH.xx.t0.ms')
params_file = os.path.join(DATA_PATH, 'sim_params.txt')
params_2file = os.path.join(DATA_PATH, 'sim_2params.txt')

class Test_Simulate():
    def test_init_ms(self):
        sim = sm.Simulate(msfile)
        nt.assert_equal(sim.msfile, msfile)
    
    def test_init_sparams(self):
        sim = sm.Simulate(sparams=params_file)
        nt.assert_equal(sim.sparams, params_file)

    def test_init_ms_sparams(self):
        sim = sm.Simulate(msfile, sparams=params_file)
        nt.assert_equal(sim.msfile, msfile)
        nt.assert_equal(sim.sparams, params_file)

    def test_read_sim_parameters(self):
        sim = sm.Simulate(msfile, sparams=params_file)
        params = sim.read_sim_parameters()
        nt.assert_equal(len(params), 5)
        np.testing.assert_equal(params[0], [50.25])
        np.testing.assert_equal(params[1], [30.78])
        np.testing.assert_equal(params[2], [1.])
        np.testing.assert_equal(params[3], [-0.7])
        np.testing.assert_equal(params[4], [150000000.])

    def test_read_sim2_parameters(self):
        sim = sm.Simulate(msfile, sparams=params_2file)
        params = sim.read_sim_parameters()
        nt.assert_equal(len(params), 5)
        np.testing.assert_equal(params[0], [50.25, 50.25])
        np.testing.assert_equal(params[1], [30.78, 30.78])
        np.testing.assert_equal(params[2], [1., 1.])
        np.testing.assert_equal(params[3], [-0.7, -0.7])
        np.testing.assert_equal(params[4], [150000000, 150000000])
    
    #def test_complist_input(self):
    #    sim = sm.Simulate(msfile, sparams=params_file)
    #    params = sim.read_sim_parameters()
    #    sim = sim.create_casa_skymodel()
    #    nt.assert_true(os.path.exists(sky_outfile))
    
    def test_complist_output(self):
        sim = sm.Simulate(msfile, sparams=params_file)
        params = sim.read_sim_parameters()
        sim = sim.create_casa_skymodel()
        nt.assert_true(os.path.exists(params_file.replace('.txt', '.cl')))

    def test_complist_flux(self):
        sim = sm.Simulate(msfile, sparams=params_file)
        params = sim.read_sim_parameters()
        sim = sim.create_casa_skymodel()
        skymodel = params_file.replace('.txt', '.cl')
        sk = rs.Skymodel(skymodel)
        flux = sk.get_flux_values()
        input_params = np.loadtxt(params_file)
        nt.assert_equal(flux[0], np.complex(input_params[2])) 
        
    def test_complist_sloc(self):
        sim = sm.Simulate(msfile, sparams=params_file)
        params = sim.read_sim_parameters()
        sim = sim.create_casa_skymodel()
        skymodel = params_file.replace('.txt', '.cl')
        sk = rs.Skymodel(skymodel)
        src_loc = sk.get_src_loc()
        input_params = np.loadtxt(params_file)
        nt.assert_equal(src_loc[0], input_params[0] * np.pi/180)
        nt.assert_equal(src_loc[1], input_params[1] * np.pi/180)

    def test_complist_freq(self):
        sim = sm.Simulate(msfile, sparams=params_file)
        params = sim.read_sim_parameters()
        sim = sim.create_casa_skymodel()
        skymodel = params_file.replace('.txt', '.cl')
        sk = rs.Skymodel(skymodel)
        freq = sk.get_freqs()
        input_params = np.loadtxt(params_file)
        nt.assert_equal(freq[0], input_params[4])

    def test_complist_sindex(self):
        sim = sm.Simulate(msfile, sparams=params_file)
        params = sim.read_sim_parameters()
        sim = sim.create_casa_skymodel()
        skymodel = params_file.replace('.txt', '.cl')
        sk = rs.Skymodel(skymodel)
        sindex = sk.get_sindex()
        input_params = np.loadtxt(params_file)
        nt.assert_equal(sindex[0], input_params[3])

