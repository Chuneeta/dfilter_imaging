from beam_solver import fits_utils as ft
import casatasks as ctk
import os

class Image():
    def __init__(self, msfile):
        self.msfile = msfile

    def generate_mfs_image(self, imagename, cell='8arcmin', imsize=512, weighting='uniform', niter=0, start=0, stop=1023, threshold='0Jy', phasecenter=''):
        ctk.tclean(self.msfile, imagename=imagename, cell=cell, imsize=imsize, weighting=weighting, spw='0:{}~{}'.format(start, stop), niter=niter, threshold=threshold, phasecenter=phasecenter)
    
    def to_fits(self, imagename, fitsname):
        ctk.exportfits(imagename=imagename, fitsimage=fitsname)

    def remove_casa_image(self, imagename):
        os.system('rm -rf {}.image')
        os.system('rm -rf {}.psf')
        os.system('rm -rf {}.residual')
        os.system('rm -rf {}.model')
        os.system('rm -rf {}.pb')
        os.system('rm -rf {}.sumwt')

