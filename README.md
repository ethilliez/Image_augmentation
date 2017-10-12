# Image_augmentation
![Alt Text 1](https://raw.github.com/ethilliez/Image_augmentation/master/example/nolib/example_b.jpg)![Alt Text 2](https://raw.github.com/ethilliez/Image_augmentation/master/example/nolib/example_k.jpg)
![Alt Text 3](https://raw.github.com/ethilliez/Image_augmentation/master/example/nolib/example_n.jpg)![Alt Text 4](https://raw.github.com/ethilliez/Image_augmentation/master/example/nolib/example_l.jpg)

## Description:
Tool to augmentate images data by performing basic geometric transformations. There are two versions of the same script: one written without much computer vision librairies and one with librairies. The examples above display image translation, rotation, contrast adjustement and image shearing performed by the script without librairies.

## Personal development goals:
- Practising basic image manipulation techniques without using libraries.
- Practising performing the same tasks using computer vision libraries.
- Preparing a tool to augment image dataset for future Neural Network training.

## Status of development:
For both scripts with and without librairies:
- Mirror flipping implemented
- Translation implemented
- Rotation implemented
- Shear implemented
- Contrast adjustment implemented
- Resizing implemented

## Requirements:
The main librairies required are: `numpy` and `skimage`,`scipy`. They can be installed using `pip install` or `conda install`.

## Execution:
1) Firstly, in `define_paths.py`:
- update the path to the folder containing the original images: `DATA_PATH`
- update the path to the folder containing the output: `OUTPUT_PATH`
2) Executing the script written without libraries: `python3 image_augmentation_nolib.py`
3) Executing the script written with librairies: `python3 image_augmentation_wlib.py`
