from beam_solver import fits_utils as ft
import casatasks as ctk
import casatools as ct
import os

class Image():
    def __init__(self, msfile):
        self.msfile = msfile

    def generate_mfs_image(self, imagename, cell='8arcmin', imsize=512, weigh:wting='uniform', niter=0, start=0, stop=1023, threshold='0Jy', phasecenter='', pblimit=0):
        #vp = ct.vpmanager()
        #vp.setpbimage(telescope='HERA', compleximage=pbimage)
        #vp.saveastable(pbimage + '.tab')
        spw = '0:{}~{}'.format(start, stop)
        ctk.tclean(self.msfile, imagename=imagename, cell=cell, imsize=imsize, weighting=weighting, spw=spw, niter=niter, threshold=threshold, phasecenter=phasecenter, pblimit=pblimit)
        ia = ct.image()
        ia.open(imagename + '.image')
        ia.maskhandler('delete', 'mask0')
        ia.close()

    def to_fits(self, imagename, fitsname, overwrite=False):
        ctk.exportfits(imagename=imagename, fitsimage=fitsname, overwrite=overwrite)

    def remove_casa_image(self, imagename):
        os.system('rm -rf {}.image')
        os.system('rm -rf {}.psf')
        os.system('rm -rf {}.residual')
        os.system('rm -rf {}.model')
        os.system('rm -rf {}.pb')
        os.system('rm -rf {}.sumwt')

