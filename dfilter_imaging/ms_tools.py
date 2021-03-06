import casatools as ct
import casatasks as ctk
import numpy as np
import os

class MSet(object):
    def __init__(self, msfile):
        self.msfile = msfile

    def open_msfile(self, nomodify=True):
        self.tb = ct.table()
        self.tb.open(self.msfile, nomodify=nomodify)

    def close_msfile(self):
        self.tb.close()

    def read_col(self, colname):
        """
        Reading data from the Measurement Set
        """
        self.open_msfile()
        data = self.tb.getcol(colname)
        self.close_msfile()
        return data

    def transfer_data(self, column_in, column_out):
        """
        Transfer data from one column to another in the Measurement Set
        """
        self.open_msfile()
        data_in = self.read_col(column_in)
        self.open_msfile(nomodify=False)
        self.tb.putcol(column_out, data_in)
        self.close_msfile()

    def get_phase_center(self):
        pc_tb = ct.table()
        pc_tb.open(os.path.join(self.msfile, 'FIELD'))
        phase_center = pc_tb.getcol('PHASE_DIR')
        pc_tb.close()
        return phase_center

    def change_phase_center(self, new_ra, new_dec):
        pc_tb = ct.table()
        pc_tb.open(os.path.join(self.msfile, 'FIELD'), nomodify=False)
        new_phase_center = np.array([new_ra, new_dec]).reshape((2, 1, 1))
        pc_tb.putcol('PHASE_DIR', new_phase_center)
        pc_tb.close()

    def convert_to_uvfits(self, uvfits_name, overwrite=False):
        """
        Convert Measurement set to uvfits file
        """
        # NOTE: The phase center shifts to (0.0, 0.0) during the conversion
        ctk.exportuvfits(self.msfile, uvfits_name, overwrite=overwrite)

    def write_data(self, data_array, column):
        self.open_msfile(nomodify=False)
        self.tb.putcol(column, data_array)
        self.tb.close()

    def add_noise_chan(self, column='DATA'):
        data = self.read_col(column)
        _sh0, _sh1, _sh2 = data.shape
        nfreq = _sh1
        for i in range(nfreq):
            data[0, i, :] = data[0, i, :] * (1 + (np.random.normal() * 1e-3))
        self.write_data(data, 'DATA')

    def get_data(self, ant0, ant1, pol, column='DATA'):
        data = self.read_col(column)
        A1 = self.read_col('ANTENNA1')
        A2 = self.read_col('ANTENNA2')
        inds = np.where((A1 == ant0) & (A2 == ant1))
        if pol=='xx': polid = 0
        data_bl = data[polid, :, inds[0]]
        return data_bl

    def set_flags_None(self):
        flags = self.read_col('FLAG')
        flags[:, :, :] = False
        self.write_data(flags, 'FLAG')
        
