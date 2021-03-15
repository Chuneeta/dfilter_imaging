import numpy as np
import casatools as ct

class Skymodel(object):
    def __init__(self, skymodel):
        self.skymodel = skymodel

    def open_skymodel(self):
        self.tb = ct.table()
        self.tb.open(self.skymodel)
        
    def close_skymodel(self):
        self.tb.close()

    def get_flux_values(self):
        self.open_skymodel()
        flux = self.tb.getcol('Flux')
        self.close_skymodel()
        return flux

    def get_src_loc(self):
        self.open_skymodel()
        sloc = self.tb.getcol('Reference_Direction')
        self.close_skymodel()
        return sloc

    def get_sindex(self):
        self.open_skymodel()
        sindex = self.tb.getcol('Spectral_Parameters')
        self.close_skymodel()
        return sindex

    def get_freqs(self):
        self.open_skymodel()
        freqs = self.tb.getcol('Reference_Frequency')
        self.close_skymodel()
        return freqs
                
