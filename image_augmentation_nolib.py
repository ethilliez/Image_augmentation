import numpy as np
import math
from scipy import ndimage, misc
from scipy.interpolate import interp1d
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
        image_trans_left = np.append(image[:,int((1-shift)*len(image[0])):,:], image[:,0:int((1-shift)*len(image[0])),:], axis = 1)
        image_trans_right = np.append(image[:,int(shift*len(image[0])):,:], image[:,0:int(shift*len(image[0])),:], axis = 1)
        image_trans_down = np.append(image[:int(shift*len(image)),:,:], image[:int((1-shift)*len(image)),:,:], axis = 0)
        image_trans_up = np.append(image[int(shift*len(image)):,:,:], image[int((1-shift)*len(image)):,:,:], axis = 0)
        return image_trans_left, image_trans_right, image_trans_up, image_trans_down

    def rotate(self, image, angle):
        angle = angle*3.14159/180.0
        image_rotated = np.zeros([len(image),len(image[0]),len(image[0][0])])
        for chan in range(0,len(image[0][0])):        
            for x in range(0,len(image)):
                for y in range(0,len(image[0])):
                	# Rotate pixels
                    xpix = x - len(image)/2
                    ypix = y - len(image[0])/2
                    newX = int(round(math.cos(angle)*(xpix) + math.sin(angle)*(ypix)))
                    newY = int(round(-math.sin(angle)*(xpix) + math.cos(angle)*(ypix)))
                    if(newX <= 0 and newY < 0):
                        newX2 = newX + int(len(image)/2)
                        newY2 = newY + int(len(image[0])/2)  
                    if(newX < 0 and newY >= 0):
                        newX2 = newX + int(len(image)/2)
                        newY2 = newY - int(len(image[0])/2)  
                    if(newX >= 0 and newY > 0):
                        newX2 = newX - int(len(image)/2)
                        newY2 = newY - int(len(image[0])/2)
                    if(newX > 0  and newY <= 0):
                        newX2 = newX - int(len(image)/2)
                        newY2 = newY + int(len(image[0])/2)                  
                    image_rotated[newX2,newY2,chan] = image[x,y,chan]
                    # Fix lost pixels by correcting with previous pixel
                    if(chan == len(image[0][0])-1 and np.array_equal(image_rotated[x,y], np.array([0,0,0])) 
                    	and np.array_equal(image_rotated[x, y-1], np.array([0,0,0])) == False):
                        image_rotated[x,y] = image_rotated[x, y-1]
       	return image_rotated

    def shearing(self, image, factor, direction='horizontal'):
        image_shear = np.zeros([len(image),len(image[0]),len(image[0][0])])
        for chan in range(0,len(image[0][0])):
            if(direction == "vertical"):
                for x in range(0,len(image)):
                    for y in range(0,len(image[0])):
                        newX = int(round(x + factor*y))
                        newY = y
                        if(newX >= len(image)-1): break 
                        image_shear[newX,newY,chan] = image[x,y,chan]                 
            elif(direction == "horizontal"):
                for x in range(0,len(image)):
                    for y in range(0,len(image[0])):
                        newX = x
                        newY = int(round(y + factor*x))
                        if(newY >= len(image[0])-1): break 
                        image_shear[newX,newY,chan] = image[x,y,chan] 
        return image_shear

    def change_contrast(self, image, factor_gain, factor_bias):
        image_contrast = np.zeros([len(image),len(image[0]),len(image[0][0])])
        for chan in range(0,len(image[0][0])):
            image_contrast[:,:,chan] = (chan+1)*factor_gain*image[:,:,chan]+factor_bias
        return image_contrast

    def resize_image(self, image, npix):
        resized_image_l = []
        # resize x axis
        for c in range(0,len(image[0][0])):
            for y in range(0,len(image)):
                f = interp1d(np.arange(0,len(image[0])), image[y,:,c], kind='cubic')
                xnew = np.linspace(0, len(image[0])-1, num=npix)
                if(y==0): 
                	resized_image_c = f(xnew)
                else:
                    resized_image_c = np.vstack((resized_image_c,f(xnew)))
            resized_image_l.append(resized_image_c)
        resized_image_a = np.dstack([resized_image_l[0],resized_image_l[1],resized_image_l[2]])
        # resize y axis
        resized_image_l = []
        for c in range(0,len(image[0][0])):
            for x in range(0,len(resized_image_a[0])):
                f = interp1d(np.arange(0,len(resized_image_a)), resized_image_a[:,x,c], kind='cubic')
                xnew = np.linspace(0, len(resized_image_a)-1, num=npix)
                if(x==0): 
                	resized_image_c = f(xnew)
                else:
                    resized_image_c = np.vstack((resized_image_c,f(xnew)))
            resized_image_l.append(resized_image_c)
        resized_image = np.dstack([resized_image_l[0],resized_image_l[1],resized_image_l[2]])
        # Fix image orientation
        for i in range(0,3):
            resized_image=np.rot90(resized_image)
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
