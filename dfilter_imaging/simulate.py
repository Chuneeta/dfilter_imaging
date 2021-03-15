from beam_solver import casa_utils as cu
from beam_solver import coord_utils as crd
import casatools as ct
import casatasks as ctk
import numpy as np

class Simulate():
    def __init__(self, msfile=None, sparams=None):
        self.msfile = msfile
        self.sparams = sparams
    
    def read_sim_parameters(self):
        params_array = np.loadtxt(self.sparams)
        return params_array[0], params_array[1], params_array[2], params_array[3], params_array[4]    

    def create_casa_skymodel(self, sky_outfile='skymodel.dat'):
        ras, decs, fluxs, sis, freqs = self.read_sim_parameters()
        cu.generate_complist_input([ras], [decs], [fluxs], [sis], [freqs], output=sky_outfile)
        self.casa_skymodel = sky_outfile.replace('.dat', '.cl')
        cu.create_complist(sky_outfile, outfile=self.casa_skymodel, delete=True)

    def generate_model_vis(self):
        """
        Generating model visibilities using skymodel
        """
        ct.ft(self.msfile, conmplist=self.casa_skymodel, usescratch=True)
        
    def transferto(self, column_in='MODEL_DATA', column_out='DATA'):
        pass
        #ct.transferto(self.msfile, "MODEL_DATA", "DATA")
    
    def to_uvfits(self, uvfits):
        pass
        #ct.ms2uvfits(self.msfile, uvfits)
