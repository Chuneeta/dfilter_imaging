from beam_solver import fits_utils as ft
from dfilter_imaging import ms_tools as mt
from beam_solver import coord_utils as crd
import casatasks as ctk
import casatools as ct
import numpy as np
import os

class Image():
    def __init__(self, msfile):
        self.msfile = msfile

    def construct_phasecenter(self, ra, dec):
        ra_s = crd.deg2hms(ra)
        dec_s = crd.deg2dms(dec)
        img_phs = 'J2000 {} {}'.format(ra_s, dec_s)
        return img_phs

    def reconstruct_phasecenter(self):
        ms = mt.MSet(self.msfile)
        phase_cnt = ms.get_phase_center()
        ra_s = crd.deg2hms(phase_cnt[0][0][0] * 180 / np.pi)
        dec_s = crd.deg2dms(phase_cnt[1][0][0] * 180/ np.pi)
        img_phs = 'J2000 {} {}'.format(ra_s, dec_s)
        return img_phs

    def generate_mfs_image(self, imagename, cell='8arcmin', imsize=512, weighting='uniform', niter=0, start=0, stop=1023, threshold='0Jy', phasecenter='', pblimit=0, ants=''):
        spw = '0:{}~{}'.format(start, stop)
        ctk.tclean(self.msfile, imagename=imagename, cell=cell, imsize=imsize, weighting=weighting, spw=spw, niter=niter, threshold=threshold, phasecenter=phasecenter, pblimit=pblimit, antenna=ants)
        ia = ct.image()
        ia.open(imagename + '.image')
        ia.maskhandler('delete', 'mask0')
        ia.close()

    def to_fits(self, imagename, fitsname, overwrite=False):
        ctk.exportfits(imagename=imagename, fitsimage=fitsname, overwrite=overwrite)

    def remove_casa_image(self, imagename):
        os.system('rm -rf {}.image'.format(imagename))
        os.system('rm -rf {}.psf'.format(imagename))
        os.system('rm -rf {}.residual'.format(imagename))
        os.system('rm -rf {}.model'.format(imagename))
        os.system('rm -rf {}.pb'.format(imagename))
        os.system('rm -rf {}.sumwt'.format(imagename))
        os.system('rm -rf {}.mask'.format(imagename))

    def plot_fitsfile(self, fitsfile, vmin=None, vmax=None, savefig=False, figname=''):
        ft.plot_fitsfile(fitsfile, vmin=vmin, vmax=vmax, savefig=savefig, figname=figname)
