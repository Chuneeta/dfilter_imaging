from beam_solver import casa_utils as cu
from beam_solver import coord_utils as crd
from dfilter_imaging import ms_tools as mt
import casatools as ct
import casatasks as ctk
import numpy as np
import os

class Simulate():
    def __init__(self, msfile=None, sparams=None):
        self.msfile = msfile
        self.sparams = sparams
    
    def read_sim_parameters(self):
        params_array = np.loadtxt(self.sparams)
        return params_array[0], params_array[1], params_array[2], params_array[3], params_array[4]    

    def create_casa_skymodel(self):
        # currently works for a single point source
        ras, decs, fluxs, sis, freqs = self.read_sim_parameters()
        directions = 'J2000 {} {}'.format(crd.deg2hms(ras), crd.deg2dms(decs))
        self.casa_skymodel = self.sparams.replace('.txt', '.cl')
        if os.path.exists(self.casa_skymodel):
            os.system('rm -rf {}'.format(self.casa_skymodel))
        cl = ct.componentlist()
        cl.addcomponent(flux=fluxs, fluxunit='Jy', polarization='Stokes', dir=directions, shape='point', freq=freqs * 1e6, spectrumtype='spectral index', index=sis)
        cl.rename(self.casa_skymodel)
        cl.close()

    def generate_model_vis(self):
        """
        Generating model visibilities using skymodel
        """
        ctk.ft(vis=self.msfile, complist=self.casa_skymodel, usescratch=True)
        
    def simulate(self):
        self.create_casa_skymodel()
        self.generate_model_vis()
        ms = mt.MSet(self.msfile)
        ms.transfer_data(column_in='MODEL_DATA', column_out='DATA')    

