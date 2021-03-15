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
        ctk.exportuvfits(self.msfile, uvfits_name, overwrite=overwrite)
