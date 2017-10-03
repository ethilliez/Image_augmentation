# Idea from: https://datascience.stackexchange.com/questions/5224/how-to-prepare-augment-images-for-neural-network
import numpy as np
from define_paths import paths
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class image_augmentation:
    def __init__(self):
        self.data_path = paths.DATA_PATH

    def read_data(self):
        logging.info(self.data_path)
        return 

	#def rotate(self,angle):
	#	return

	#def translation(self,shift):
	#	return

	#def rescale(self,factor):
	#	return

	#def shearing(self,angle):
	#	return

	#def perform_augmentation(self):



if __name__ == '__main__':
	process = image_augmentation()
	process.read_data()
	#process.perform_augmentation()