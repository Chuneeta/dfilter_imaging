import pyuvdata
from uvtools import dspec
import copy
import numpy as np
#from dfilter_imaging import uvfits_tools as uf

MYCACHE = {}
c = 3e8
#telescope_location = np.array([ 5109325.85521063,  2005235.09142983, -3239928.42475396])

ants = np.array([136, 140, 121,  88,  41,  86,  36,  51,  50,  98, 123, 124,  65,
       137,  82, 120, 143,  66,  83, 122,  67,  68,  69,  70,  71,  85,
         0,   1,  11,  12,  13,  14,   2,  23,  24,  25,  26,  27,  37,
        38,  39,  40,  52,  53,  54,  55,  84,  87, 141, 138, 142, 139])

enu_pos = np.array([[-1.56597561e+02,  2.94391631e+00, -1.81921107e-01],
       [-9.81661978e+01,  3.16706292e+00, -3.00755454e-01],
       [-9.08139441e+01, -9.46184684e+00, -1.70652904e-01],
       [-4.68937941e+01, -3.45980880e+01,  1.69733574e-01],
       [-5.40527841e+01, -7.25763846e+01,  4.89356640e-01],
       [-7.61094735e+01, -3.47096619e+01,  7.94515411e-02],
       [-1.27091991e+02, -7.28553234e+01,  4.78317338e-01],
       [-1.19836404e+02, -6.01706233e+01,  3.38590440e-01],
       [-1.34444245e+02, -6.02264109e+01,  3.28299023e-01],
       [-1.56500935e+02, -2.23596873e+01,  1.18042599e-01],
       [-6.15982651e+01, -9.35027320e+00, -1.30304031e-01],
       [-4.69904257e+01, -9.29448635e+00, -1.30179728e-01],
       [-1.41796462e+02, -4.76075046e+01,  2.38247069e-01],
       [-1.41989718e+02,  2.99970292e+00, -3.11579559e-01],
       [-1.34540837e+02, -3.49328110e+01,  1.18486419e-01],
       [-1.05421784e+02, -9.51763369e+00, -1.70877473e-01],
       [-5.43426798e+01,  3.33442291e+00, -2.90232146e-01],
       [-1.27188621e+02, -4.75517171e+01,  2.28555194e-01],
       [-1.19932995e+02, -3.48770236e+01,  8.87778334e-02],
       [-7.62061045e+01, -9.40606002e+00, -1.50461757e-01],
       [-1.12580779e+02, -4.74959295e+01,  2.08829898e-01],
       [-9.79729376e+01, -4.74401419e+01,  1.79071181e-01],
       [-8.33650972e+01, -4.73843546e+01,  1.99279042e-01],
       [-6.87572570e+01, -4.73285674e+01,  2.29453479e-01],
       [-5.41494176e+01, -4.72727808e+01,  3.39594494e-01],
       [-9.07173138e+01, -3.47654491e+01,  7.92603972e-02],
       [-1.05035302e+02, -1.10722053e+02,  9.38171198e-01],
       [-9.04274589e+01, -1.10666264e+02,  9.28395773e-01],
       [-1.12387519e+02, -9.81031445e+01,  7.88253403e-01],
       [-9.77796757e+01, -9.80473552e+01,  7.18494688e-01],
       [-8.31718330e+01, -9.79915661e+01,  6.58702549e-01],
       [-6.85639930e+01, -9.79357801e+01,  7.98876989e-01],
       [-7.58196165e+01, -1.10610476e+02,  9.18586923e-01],
       [-1.19739775e+02, -8.54742312e+01,  6.48302214e-01],
       [-1.05131933e+02, -8.54184435e+01,  6.68560208e-01],
       [-9.05240908e+01, -8.53626554e+01,  6.58784778e-01],
       [-7.59162490e+01, -8.53068673e+01,  6.48975932e-01],
       [-6.13084085e+01, -8.52510807e+01,  7.49133657e-01],
       [-1.12484151e+02, -7.27995366e+01,  5.68592042e-01],
       [-9.78763087e+01, -7.27437487e+01,  5.58833325e-01],
       [-8.32684667e+01, -7.26879606e+01,  5.29041185e-01],
       [-6.86606257e+01, -7.26321730e+01,  5.49215625e-01],
       [-1.05228564e+02, -6.01148364e+01,  4.08848436e-01],
       [-9.06207219e+01, -6.00590485e+01,  3.79073005e-01],
       [-7.60128810e+01, -6.00032610e+01,  3.89264156e-01],
       [-6.14050399e+01, -5.99474731e+01,  3.59421881e-01],
       [-1.05325155e+02, -3.48212364e+01,  8.90358257e-02],
       [-6.15016336e+01, -3.46538748e+01,  9.96092693e-02],
       [-8.35583582e+01,  3.22284958e+00, -3.00547597e-01],
       [-1.27381877e+02,  3.05548959e+00, -3.11271434e-01],
       [-6.89505189e+01,  3.27863625e+00, -2.90373161e-01],
       [-1.12774037e+02,  3.11127625e+00, -3.20996736e-01]])


class Filter(object):
    def __init__(self, uvfits):
        self.uvfits = uvfits

    def get_filter(self, freqs, data, wgts, bl_length, suppression_factors=[1e-9], mode='dayenu'):
        bl_delay = bl_length / c
        model, resid, info = dspec.fourier_filter(x=freqs, data=data, wgts=wgts,
                                              mode=mode, filter_centers=[0.], skip_wgt=0.1,
                                              filter_half_widths=[bl_delay], suppression_factors=suppression_factors,
                                              cache=MYCACHE, max_contiguous_edge_flags=20)

        return model, resid, info

    def filter_ants(self, cut_bl):
        self.filtered_bls = []
        for i, a1 in enumerate(ants):
            ind1 = np.where(ants == a1)
            for j, a2 in enumerate(ants[i+1:]):
                ind2 = np.where(ants == a2)
                bl_length = np.sqrt((enu_pos[ind1][0][0] - enu_pos[ind2][0][0])**2 + (enu_pos[ind1][0][1] - enu_pos[ind2][0][1])**2)
                if bl_length <= cut_bl:
                    self.filtered_bls.append((a1, a2))

    def apply_filter(self, bl_cut, bl_length=None, scale=1):
        uvf = pyuvdata.UVData()
        uvf.read_uvfits(self.uvfits, run_check=False)
        freqs = uvf.freq_array[0]
        if uvf.timesys == 'TAI': uvf.timesys = 'UTC'
        mod_uvf = copy.deepcopy(uvf)
        res_uvf = copy.deepcopy(uvf)
        self.filter_ants(bl_cut)
        for bl in self.filtered_bls:
            print ('Bl: {}'.format(bl))
            if bl[1] < bl[0]:
                bl = bl[::-1] 
            inds = uvf.antpair2ind(bl)
            data_bl = uvf.get_data(bl)
            wgts = np.ones(data_bl.shape)
            if bl_length is None:
                ind1 = np.where(ants == bl[0])
                ind2 = np.where(ants == bl[1])
                bl_length = np.sqrt((enu_pos[ind1][0][0] - enu_pos[ind2][0][0])**2 + (enu_pos[ind1][0][1] - enu_pos[ind2][0][1])**2)
            model, resid, info = self.get_filter(freqs, data_bl, wgts, scale * bl_length, mode='dayenu')
            mod_uvf.data_array[inds, 0, :, 0] = model
            res_uvf.data_array[inds, 0, :, 0] = resid
    
        mod_uvf.write_uvfits(self.uvfits + 'F', run_check=False, check_extra=False)
        res_uvf.write_uvfits(self.uvfits + 'B', run_check=False, check_extra=False)
