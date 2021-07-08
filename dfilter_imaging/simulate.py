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
        if params_array.ndim == 1:
            return [params_array[0]], [params_array[1]], [params_array[2]], [params_array[3]], [params_array[4]]  
        else:
            return params_array[:,0].tolist(), params_array[:,1].tolist(), params_array[:,2].tolist(), params_array[:,3].tolist(), params_array[:,4].tolist()
    
    def create_casa_skymodel(self):
        # currently works for a single point source
        sim_parameters = self.read_sim_parameters()
        ras, decs, fluxs, sis, freqs = sim_parameters[0], sim_parameters[1], sim_parameters[2], sim_parameters[3], sim_parameters[4]        
        directions = ['J2000 {} {}'.format(crd.deg2hms(ra), crd.deg2dms(dec)) for ra, dec in zip(ras, decs)]
        self.casa_skymodel = self.sparams.replace('.txt', '.cl')
        if os.path.exists(self.casa_skymodel):
            os.system('rm -rf {}'.format(self.casa_skymodel))
        cl = ct.componentlist()
        for i in range(len(fluxs)):
            cl.addcomponent(flux=fluxs[i], fluxunit='Jy', polarization='Stokes', dir=directions[i], shape='point', freq=freqs[i], spectrumtype='spectral index', index=sis[i])
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
        # setting flag to False
        flags = ms.read_col('FLAG')
        flags[:, :, :] = False
