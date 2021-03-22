import pyuvdata
import casatasks as ctk

class UVfits(object):
    def __init__(self, uvfits):
        self.uvfits = uvfits

    def read_uvfits(self):
        self.uvf = pyuvdata.UVData()
        self.uvf.read_uvfits(self.uvfits)

    def convert_to_ms(self, msname):
        ctk.importuvfits(self.uvfits, msname)
