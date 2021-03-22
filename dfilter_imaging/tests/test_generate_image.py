from dfilter_imaging import generate_image as gi
from dfilter_imaging.data import DATA_PATH
import nose.tools as nt
import os

msfile = os.path.join(DATA_PATH, 'zen.2458114.31193.HH.xx.t0.ms')

class Test_Image():
    def test__init__(self):
        img = gi.Image(msfile)
        nt.assert_equal(img.msfile, msfile)

    def test_generate_mfs_image(self):
        img = gi.Image(msfile)
        imagename = os.path.join(DATA_PATH, '2458114.31193.HH.xx.t0')
        img.generate_mfs_image(imagename)
        nt.assert_true(os.path.exists(imagename + '.image'))
        nt.assert_true(os.path.exists(imagename + '.residual'))
        nt.assert_true(os.path.exists(imagename + '.psf'))
        nt.assert_true(os.path.exists(imagename + '.pb'))
        nt.assert_true(os.path.exists(imagename + '.sumwt'))
        img.remove_casa_image(imagename)

    def test_generate_mfs_image(self):
        img = gi.Image(msfile)
        imagename = os.path.join(DATA_PATH, '2458114.31193.HH.xx.t0')
        img.generate_mfs_image(imagename)
        fitsname = imagename + '.fits'
        #img.to_fits(imagename + '.image', fitsname)
        img.remove_casa_image(imagename)
        nt.assert_true(os.path.exists(fitsname))

