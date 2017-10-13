class paths:
    DATA_PATH='example/'  # Folder path where raw images are stored
    OUTPUT_PATH='example/nolib/'  # Folder which contains the output images

class parameters:
	SIZE_IMAGE = 250  # Size of output images in pixels
	TRANSLATION = 0.1  # Fraction of the image size to be translated
	ROTATION = 15.0  # Angle of rotation in degrees
	SHEARING = 0.12  # Shearing factor
	CONTRAST = [0.33,15]  # Gain and Bias for contrast adjustement 
    