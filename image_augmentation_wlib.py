import numpy as np
import math
from scipy import ndimage, misc
from skimage import transform, exposure
import re
import matplotlib.pyplot as plt
from glob import glob
from define_paths import paths
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class image_augmentation:
    def __init__(self):
        self.data_path = paths.DATA_PATH
        self.output_path = paths.OUTPUT_PATH
        self.test = False

    def _read_data(self, file):
        image = misc.imread(file)
        return image

    def mirror_rotate(self, image, direction='horizontal'):
        if(direction == 'horizontal'):
            image_mirror = image[:,::-1,:]
        elif(direction == 'vertical'):
            image_mirror = image[::-1,:,:]
        return image_mirror

    def translation(self, image, shift):
        factor = int(shift*len(image))
        affine_tf = transform.AffineTransform(scale=(1.0,1.0),translation=(-factor,0))
        image_trans_left = transform.warp(image, inverse_map=affine_tf)
        affine_tf = transform.AffineTransform(scale=(1.0,1.0),translation=(0,-factor))
        image_trans_down = transform.warp(image, inverse_map=affine_tf)
        affine_tf = transform.AffineTransform(scale=(1.0,1.0),translation=(factor,0))
        image_trans_right = transform.warp(image, inverse_map=affine_tf)
        affine_tf = transform.AffineTransform(scale=(1.0,1.0),translation=(0,factor))
        image_trans_up = transform.warp(image, inverse_map=affine_tf)
        return image_trans_left, image_trans_right, image_trans_up, image_trans_down

    def rotate(self, image, angle):
        image_rotated = ndimage.rotate(image, angle, reshape=False)
       	return image_rotated

    def shearing(self, image, factor, direction='horizontal'):
        affine_tf = transform.AffineTransform(shear=factor)
        # Apply transform to image data
        image_shear = transform.warp(image, inverse_map=affine_tf)    
        return image_shear

    def change_contrast(self, image, factor_gain, factor_bias):
        image_contrast = exposure.rescale_intensity(image, in_range=(factor_gain*factor_bias,(8+factor_gain)*factor_bias))
        return image_contrast

    def resize_image(self, image, npix):
        resized_image = misc.imresize(image,(npix,npix))
        return resized_image

    def save_image(self, image, ori_file, number):
        # Use Regular Expression to get the name of the Data folder
        count_slash = self.data_path.count('/')
        pattern=""
        for i in range(count_slash-1):
            pattern=pattern+".*/"
        pattern=pattern+"(.*?)/"
        # Save the image using the Data folder as name
        for i in range(0,len(image)):
            misc.imsave(self.output_path+re.search(pattern,self.data_path).group(1)
                       +"_"+number[i]+".jpg",image[i])

    def plot_image(self, image):
        plt.imshow(image)
        plt.show() 

    def perform_augmentation(self,npix):
    	# List all images within folder
        filelist = glob(self.data_path+'*[a-zA-Z0-9].*')
        logger.info(("All images to be augmented are: ", filelist))
        #--
        # Set size for all images
        logger.info(("Image size: ",npix))
        #--
        # Tranformation for each image
        for file in filelist:
            logger.info(("Performing transformation for image: ", file))
            # Read image and resize it
            image = self._read_data(file)
            image = self.resize_image(image, npix)
            self.save_image([image],file,["z"])
            # Perform mirror rotation and save
            image_mirror = self.mirror_rotate(image)
            self.save_image([image_mirror],file,["a"])
            # Perform translation on original image and save
            image_trans_left, image_trans_right, image_trans_up, image_trans_down = self.translation(image, 0.1)
            self.save_image([image_trans_left, image_trans_right, image_trans_up, image_trans_down],file,["b","c","d","e"])
            # Perform translation on mirror image and save
            image_trans_left, image_trans_right, image_trans_up, image_trans_down = self.translation(image_mirror, 0.1)
            self.save_image([image_trans_left, image_trans_right, image_trans_up, image_trans_down],file,["f","g","h","i"])
            # Perform rotation on original image and save
            image_rotated = self.rotate(image,15.0)
            self.save_image([image_rotated],file,["j"])
            # Perform rotation on mirror image and save
            image_rotated = self.rotate(image_mirror,15.0)
            self.save_image([image_rotated],file,["k"])
            # Perform shearing on original image and save
            image_shear = self.shearing(image, 0.12)
            self.save_image([image_shear],file,["l"])
            # Perform shearing on mirror image and save
            image_shear = self.shearing(image_mirror, 0.12)
            self.save_image([image_shear],file,["m"])
            # Perform change contrast on original image and save
            image_contrast = self.change_contrast(image, 0.33, 15)
            self.save_image([image_contrast],file,["n"])
            # Perform change contrast on mirror image and save
            image_contrast = self.change_contrast(image_mirror, 0.33, 15)
            self.save_image([image_contrast],file,["o"])
            # Limit to the first image for testing
            if(self.test):
                logger.info("Stopping after the first image.")
                exit()


if __name__ == '__main__':
	process = image_augmentation()
	process.perform_augmentation(npix=400)
