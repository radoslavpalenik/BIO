import cv2
import sys
import os
import helper
import fnmatch
from matplotlib import pyplot as plt
from skimage.filters import frangi, hessian

# source: https://github.com/donblob/v_ex

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
                img = cv2.flip(input_image, 1)

                # get image parameters
                height, width = img.shape[:2]
                # get starting pixel coords (top left of cropped bottom)
                start_row, start_col = int(height * .5), int(0)
                # get ending pixel coords (bottom right of cropped bottom)
                end_row, end_col = int(height), int(width)
               # cropped_bot = img[start_row:end_row, start_col:end_col]
               # img = cropped_bot

                # blur image to reduce noise

                # equalize the histogram to improve contrast
                img_eq = cv2.equalizeHist(img)
                cv2.imshow('2_img_eq', img_eq)

                # create Contrast Limited Adaptive Histogram Equalization
                clahe = cv2.createCLAHE(clipLimit=9.0, tileGridSize=(10, 10))
                cl1 = clahe.apply(img_eq)
                cv2.imshow('3_cl1', cl1)

                img_blur = cv2.medianBlur(cl1, 5)
                cv2.imshow('3.1_img_blur', img_blur)
                
                cl1 = cl1.max()-cl1
                cl1 = cl1.astype(float)
            
                cv2.imshow('inverted', cl1)
                cv2.imshow('3.1_frangi_inv', frangi(cl1, black_ridges=False))

                # set global threshold value to eliminate grey values (binary)
                th0 = cv2.adaptiveThreshold(img_eq, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 3)
                cv2.imshow('4_th0', th0)

                # median to reduce noise
                median = cv2.medianBlur(th0, 3)
                cv2.imshow('5_median', median)
                # blur to smooth edges
                blur = cv2.GaussianBlur(median, (3, 3), 0)
                cv2.imshow('6_blur', blur)

                while(1):
                    k = cv2.waitKey(5) & 0xFF
                    if k == 27:
                        break
                
                cv2.destroyAllWindows()

                # save to disk
                cv2.imwrite(output_file, blur)
                print(f'Success! File {output_file} has been written. It was file with number: {counter}')
