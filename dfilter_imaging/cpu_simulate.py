from hera_sim.visibilities import VisCPU
from hera_sim import io
import numpy as np
import healpy
import matplotlib.pyplot as plt
import pyuvsim
from pyuvsim.analyticbeam import AnalyticBeam
from astropy.units import sday
import matplotlib as mpl
import os
from pygdsm import GlobalSkyModel2016
from pygdsm import GlobalSkyModel
import healpy as hp
import pyuvdata
from beam_solver import fits_utils as ft


class Simulate(object):
    def __init__(self, antpos):
        self.antpos = antpos

    def myuvdata(self, ntimes, nfreqs, ants={}, start_freq=100e6, **kwargs): 
        return io.empty_uvdata(nfreq = nfreqs,
                               channel_width = start_freq / nfreqs,
                               integration_time=sday.to('s')/ntimes,
                               ntimes=ntimes, ants=ants, **kwargs)

    def diffuse_foregrounds(self, freqs, nside):
        # generating diffuse maps
        gsm_2016 = GlobalSkyModel2016(freq_unit='MHz')
        #gsm_maps = gsm_2016.generate(freqs)  
        #gsm_maps = hp.ud_grade(gsm_maps, nside)
        # generating diffuse maps
        gsm_150 = gsm_2016.generate(150)  
        gsm_150 = hp.ud_grade(gsm_150, 32)
        gsm_maps = np.zeros((len(freqs), gsm_150.shape[0]))
        for i in range(len(freqs)):
            gsm_maps[i,:] = gsm_150 * (freqs[i] * 1e-6 / 150.)**-2.7
        return gsm_maps


    def simulate_diffuse(self, ntimes, nfreqs, I_sky=None, nside=128, beam_type='gaussian', diameter=14.0):
        self.uvdata = self.myuvdata(ntimes, nfreqs, ants=self.antpos)
        freqs = self.uvdata.freq_array[0]
        if I_sky is None: 
            I_sky = self.diffuse_foregrounds(freqs, nside=nside)
        beam = AnalyticBeam(beam_type, diameter=diameter)
        beams = np.repeat([beam], len(self.antpos.keys())) 
        vis_cpu = VisCPU(uvdata=self.uvdata, sky_intensity=I_sky, beams=beams)        
        return vis_cpu.simulate()

    def write_to_uvh5(self, filename):
        self.uvdata.write_uvh5(filename)

    def write_to_uvfits(self, filename):
         self.uvdata.write_uvfits(filename, force_phase=True, spoof_nonessential=True)
    
    
