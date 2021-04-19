import pyuvdata
import casatasks as ctk
import os, sys

class UVfits(object):
    def __init__(self, uvfits):
        self.uvfits = uvfits

    def read_uvfits(self):
        self.uvf = pyuvdata.UVData()
        self.uvf.read_uvfits(self.uvfits)

    def convert_to_ms(self, msname, overwrite=False):
        if overwrite:
            os.system('rm -rf {}'.format(msname))
        ctk.importuvfits(self.uvfits, msname)
