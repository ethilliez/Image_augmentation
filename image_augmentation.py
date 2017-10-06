# Idea from: https://datascience.stackexchange.com/questions/5224/how-to-prepare-augment-images-for-neural-network
import numpy as np
from scipy import ndimage, misc
import matplotlib.pyplot as plt
from glob import glob
from define_paths import paths
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class image_augmentation:
    def __init__(self):
        self.data_path = paths.DATA_PATH
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
        image_trans_left = np.append(image[:,int((1-shift)*len(image[0])):,:], image[:,0:int((1-shift)*len(image[0])),:], axis = 1)
        image_trans_right = np.append(image[:,int(shift*len(image[0])):,:], image[:,0:int(shift*len(image[0])),:], axis = 1)
        image_trans_down = np.append(image[:int(shift*len(image)),:,:], image[:int((1-shift)*len(image)),:,:], axis = 0)
        image_trans_up = np.append(image[int(shift*len(image)):,:,:], image[int((1-shift)*len(image)):,:,:], axis = 0)
        return image_trans_left, image_trans_right, image_trans_up, image_trans_down

   # def rotate(self, image, angle):
   #     image_rotated = 
   # 	return image_rotated

    #def shearing(self, image, factor):
    # IN PROGRESS
    #    shear_factor = np.array([[1,0],[factor,1]])
    #    image_shear = np.zeros(len(image),len(image[0]),len(image[0][0]))
    #    for chan in image[0][0]:
    #        for x in image[0]:
    #    	    for y in image:
    #                vector = np.array(x,y)
    #    	    	shear_pixel = np.multiply(shear_factor,vector)
    #                x_new = shear_pixel[0]
    #                y_new = shear_pixel[1]
    #    plt.imshow(image)
    #    plt.show() 
    #    plt.imshow(image_shear)
    #    plt.show()
    #    print(image.shape)
    #    print(image_shear.shape)
    #    exit()
    #    return image_shear

	# def resize(self,image,nx,ny):
    #   return

    def save_image(self, image, ori_file, number):
    	for i in range(0,len(image)):
    	    misc.imsave(ori_file[:-4]+number[i]+".jpg",image[i])

    def perform_augmentation(self, folder):
    	# List all images within folder
        path = self.data_path + folder
        filelist = glob(path+'*')
        logger.info(filelist)
        # for each image
        i = 0
        for file in filelist:
        	# Read image
            image = self._read_data(file)
            # Perform mirror rotation and save
            image_mirror = self.mirror_rotate(image)
            self.save_image([image_mirror],file,["a"])
            # Perform translation on original image and save
            image_trans_left, image_trans_right, image_trans_up, image_trans_down = self.translation(image, 0.1)
            self.save_image([image_trans_left, image_trans_right, image_trans_up, image_trans_down],file,["b","c","d","e"])
            # Perform translation on mirror image and save
            image_trans_left, image_trans_right, image_trans_up, image_trans_down = self.translation(image_mirror, 0.1)
            self.save_image([image_trans_left, image_trans_right, image_trans_up, image_trans_down],file,["f","g","h","i"])
            # Perform shearing on original image and save
            #image_shear = self.shearing(image, 3)
            #self.save_image([image_shear],file,["j"])
            # Limit to the first image for testing
            if(self.test):
                logger.info("Stopping after the first image.")
                exit()



if __name__ == '__main__':
	process = image_augmentation()
	process.perform_augmentation('Elo/')