import cv2
import sys
import os
import helper
import fnmatch
import numpy as np
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
                height, width = img.shape[:2]

                #canny filter
                cv2.imshow('0_img', img)

                # Applying CLAHE
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                cl = clahe.apply(img)

                cv2.imshow('Result', cl)

                img_canny = cv2.medianBlur(cl, 5)
                med_val = np.median(img_canny)
                lower = int(max(0 ,0.5*med_val))
                upper = int(min(255,1*med_val))

                cv2.imshow('0_img-blurred', img_canny)
                img_canny = cv2.Canny(img_canny, lower, upper)
                cv2.imshow('2_canny_afterBlur', img_canny)



                #Dilates finger lines to connect perimeter walls
                dil_matrix = np.ones((2,30), np.uint8) 
                d_im = cv2.dilate(img_canny, dil_matrix, iterations=3)
                cv2.imshow('Initiation of mask creation', d_im)

                #Gets contours of perimeter walls
                contours, hierarchy = cv2.findContours(d_im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                contour_area = []

                for c in contours:
                    contour_area.append((cv2.contourArea(c), c))

                contour_area = sorted(contour_area, key=lambda x:x[0], reverse=True)
                
                mask = np.zeros((height, width, 3), dtype = "uint8")

                coords = np.vstack([contour_area[0][1], contour_area[1][1]])

                cv2.fillPoly(mask, [coords], (255, 255, 255))
                cv2.imshow('Initial contours',mask)

                #Erodes perimeter walls to make finger mask more accurate
                er_matrix = np.ones((1,10), np.uint8)
                e_im = cv2.erode(mask, er_matrix, iterations=2) 

                cv2.imshow('After erosion', e_im)

                em_gray = cv2.cvtColor(e_im, cv2.COLOR_BGR2GRAY)

                contours, hierarchy = cv2.findContours(em_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                contour_area = []

                print(contours)

                for c in contours:
                    contour_area.append((cv2.contourArea(c), c))

                #Finds extremes of contours to get finger perimeter
                c = contour_area[0][1]
                top_left_ext = tuple(c[c[:, :, 0].argmin()][0])
                top_right_ext = tuple(c[c[:, :, 0].argmax()][0])

                c = contour_area[1][1]
                print(c[c[:, :, 0].argmin()][0])
                bot_left_ext = tuple(c[c[:, :, 0].argmin()][0])
                bot_right_ext = tuple(c[c[:, :, 0].argmax()][0])
                
                #Draws contours for debugging
                
                #cv2.drawContours(e_im, contours, -1, (0,120,0), 3)
                #cv2.circle(e_im, top_left_ext, 4, (0, 0, 128), -1)
                #cv2.circle(e_im, top_right_ext, 4, (0, 255, 0), -1)
                #cv2.circle(e_im, bot_left_ext, 4, (128, 0, 128), -1)
                #cv2.circle(e_im, bot_right_ext, 4, (0, 255, 255), -1)


                #Creates perimeter in the image

                cv2.line(e_im, top_left_ext, bot_left_ext, (255,255,255), 2)
                cv2.line(e_im,top_right_ext, bot_right_ext, (255,255,255), 2)

                cv2.imshow('Connected contours', e_im)

                #Creates Mask

                em_gray = cv2.cvtColor(e_im, cv2.COLOR_BGR2GRAY)
                contours, hierarchy = cv2.findContours(em_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                print("***************\n",contours)

                cv2.drawContours(e_im, contours, -1, (255,255,255), thickness=cv2.FILLED)
                cv2.imshow('Mask', e_im)



                # get image parameters
                height, width = img.shape[:2]
                # get starting pixel coords (top left of cropped bottom)
                start_row, start_col = int(height * .5), int(0)
                # get ending pixel coords (bottom right of cropped bottom)
                end_row, end_col = int(height), int(width)

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
                
                cl1 = frangi(cl1, black_ridges=False)
                cv2.imshow('3.1_frangi_inv', cl1)

                med_val = np.median(cl1)
                lower = int(max(0, med_val))
                upper = int(min(255, 2*med_val))

                # set global threshold value to eliminate grey values (binary)
                #th0 = cv2.adaptiveThreshold(img_eq, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 3)
                #cv2.imshow('4_th0', th0)

                # median to reduce noise
                #median = cv2.medianBlur(th0, 3)
                #cv2.imshow('5_median', median)
                # blur to smooth edges
                #blur = cv2.GaussianBlur(median, (3, 3), 0)
                #cv2.imshow('6_blur', blur)

                while(1):
                    k = cv2.waitKey(5) & 0xFF
                    if k == 27:
                        break
                
                cv2.destroyAllWindows()

                # save to disk
                cv2.imwrite(output_file, cl1)
                print(f'Success! File {output_file} has been written. It was file with number: {counter}')
