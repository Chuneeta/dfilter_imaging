from astropy.time import Time
import pyuvdata
import casatasks as ctk
import os, sys

class UVfits(object):
    def __init__(self, uvfits):
        self.uvfits = uvfits

    def read_uvfits(self):
        self.uvf = pyuvdata.UVData()
        self.uvf.read_uvfits(self.uvfits, run_check=False)

    def phase_to_time(self, time=None):
        self.read_uvfits()
        times = self.uvf.time_array
        phs_time = times[int(len(times)/2.)] if time is None else time
        print ('Phasing visibilities to {}'.format(phs_time))
        self.uvf.phase_to_time(Time(phs_time, format='jd', scale='utc'))

    def convert_to_ms(self, msname, overwrite=False):
        if overwrite:
            os.system('rm -rf {}'.format(msname))
        ctk.importuvfits(self.uvfits, msname)
