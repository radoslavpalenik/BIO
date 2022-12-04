# BIO Project
# Authors:  Radoslav Páleník <xpalen05@stud.fit.vutbr.cz>, Jozef Čabala <xcabal07@stud.fit.vutbr.cz>, Jana Gregorová <xgrego20@stud.fit.vutbr.cz>
# Name: Finger blood vessel detection from multiple viewpoints
# Date 2022-12-04
import cv2
import sys
import os
import helper
import fnmatch
from matplotlib import pyplot as plt
from skimage.filters import frangi, hessian
from skimage.morphology import skeletonize

import imageExtractor as extractor

def start(dir_path, data_directory_name, output_directory_name):
    data_directory_path = dir_path + "/" + data_directory_name 

    # create dir for saving each angel of finger photos
    helper.ifDirNotExistCreate(output_directory_name)

    counter = 0

    # extraction of veins and saving them to corresponding dir
    for root, dirs, files in os.walk(dir_path + "/" + str(data_directory_name)):
        for dir in dirs: 
            helper.ifDirNotExistCreate(output_directory_name + root[len(data_directory_path):] + "/" + dir)

        for file in files:
            if fnmatch.fnmatch(file, '*.png'):
                counter += 1
                output_file = output_directory_name + root[len(data_directory_path):] + "/" + file[:-4] + "_veins_extractions.bmp" 
                

                # load images
                input_image = cv2.imread(root + "/" + file, 0)

                img_canny = extractor.image_preparator(input_image)
                height, width = img_canny.shape[:2]

                e_im = extractor.mask_constructor(img_canny, height, width);
               
                img = extractor.vein_extractor(input_image, e_im, height, width)
                 
                # save to disk
                cv2.imwrite(output_file, img)
                print(f'Success! File {output_file} has been written. It was file with number: {counter}')
