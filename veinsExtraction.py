import cv2
import sys
import os
import helper
import fnmatch
import numpy as np
from tensorflow.keras.utils import img_to_array
from matplotlib import pyplot as plt
from skimage.filters import frangi, hessian
from skimage.morphology import skeletonize


def mask_constructor(img_canny, height, width):
    

    contours, hierarchy = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #Erases minor artifacts in image 
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if h<50 and w<50: 
            cv2.fillConvexPoly(img_canny,contour,0) 

    #Connects nearby edges with closing operation
    closing = cv2.morphologyEx(img_canny, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (200,20)));
    cv2.imshow('Canny closing', closing)

    #Dilates finger lines to connect perimeter walls
    dil_matrix = np.ones((2,30), np.uint8) 
    d_im = cv2.dilate(closing, dil_matrix, iterations=3)
    cv2.imshow('Initiation of mask creation', d_im)

    #Gets contours of perimeter walls
    contours, hierarchy = cv2.findContours(d_im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contour_area = []

    if len(contours) > 1:

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

        print(len(contours))

        for c in contours:
            contour_area.append((cv2.contourArea(c), c))

        #Finds extremes of contours to get finger perimeter
        c = contour_area[0][1]
        bot_left_ext = tuple(c[c[:, :, 0].argmin()][0])
        bot_right_ext = tuple(c[c[:, :, 0].argmax()][0])

        c = contour_area[1][1]
        top_left_ext = tuple(c[c[:, :, 0].argmin()][0])
        top_right_ext = tuple(c[c[:, :, 0].argmax()][0])
        
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

        
        if bot_left_ext[0] > 150:
            print("BL RED: ",bot_left_ext)
            cv2.line(e_im, (20, bot_left_ext[1]), bot_left_ext,(255,255,255), 2 )
            bot_left_ext = ((20, bot_left_ext[1]))
        if top_left_ext[0] > 150:
            print("TL GREEN: ",top_left_ext)
            cv2.line(e_im, (20, top_left_ext[1]), top_left_ext,(255,255,255), 2 )
            top_left_ext = (20, top_left_ext[1])
        cv2.line(e_im, top_left_ext, bot_left_ext, (255,255,255), 2)
        


        if bot_right_ext[0] < 450:
            print("BR BLUE: ",bot_right_ext)
            cv2.line(e_im, bot_right_ext, (580, bot_right_ext[1]), (255,255,255), 2 )
            bot_right_ext =(580, bot_right_ext[1])
        if top_right_ext[0] < 450:
            print("TR XXX: ",top_right_ext)
            cv2.line(e_im, top_right_ext, ( 580, top_right_ext[1]), (255,255,255), 2 )
            top_right_ext = ( 580, top_right_ext[1])
        cv2.line(e_im,top_right_ext, bot_right_ext, (255,255,255), 2)

        em_gray = cv2.cvtColor(e_im, cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(em_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        cv2.drawContours(e_im, contours, -1, (255,255,255), thickness=cv2.FILLED)
        

        cv2.imshow('Mask', e_im)

        #Erodes perimeter walls to make finger mask more accurate
        er_matrix = np.ones((5,2), np.uint8)
        e_im = cv2.erode(e_im, er_matrix, iterations=2) 

        cv2.imshow('Thinner mask', e_im)
        print(e_im.shape)


    else:
        print("1 Contour")
        er_matrix = np.ones((5,2), np.uint8)
        e_im = cv2.erode(d_im, er_matrix, iterations=2) 
        e_im = cv2.cvtColor(e_im,cv2.COLOR_GRAY2RGB)

        
        cv2.circle(e_im, (100,100), 8, (255, 0, 255), -1)
        print(e_im.shape)

    return e_im


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

                #-cv2.imshow('Result', cl)

                img_canny = cv2.medianBlur(cl, 5)
                med_val = np.median(img_canny)
                lower = int(max(0 ,0.5*med_val))
                upper = int(min(255,1*med_val))

                #-cv2.imshow('0_img-blurred', img_canny)
                img_canny = cv2.Canny(img_canny, lower, upper)
                cv2.imshow('2_canny_afterBlur', img_canny)


                e_im = mask_constructor(img_canny, height, width);

                # get image parameters
                height, width = img.shape[:2]
                # get starting pixel coords (top left of cropped bottom)
                start_row, start_col = int(height * .5), int(0)
                # get ending pixel coords (bottom right of cropped bottom)
                end_row, end_col = int(height), int(width)

                # blur image to reduce noise
                # equalize the histogram to improve contrast
                img_eq = cv2.equalizeHist(img)
                #-cv2.imshow('2_img_eq', img_eq)

                # create Contrast Limited Adaptive Histogram Equalization
                clahe = cv2.createCLAHE(clipLimit=9.0, tileGridSize=(10, 10))
                cl1 = clahe.apply(img_eq)
                #-cv2.imshow('3_cl1', cl1)

                #img_blur = cv2.medianBlur(cl1, 9)
                img_blur = cv2.bilateralFilter(cl1, 9, 75, 75)
                #-cv2.imshow('3.1_img_blur', img_blur)
                
                cl1 = cl1.max()-cl1
                cl1 = cl1.astype(float)
                cl1 = np.float32(cl1)
                
                cl1 = frangi(cl1, black_ridges=False)
                franghi = cl1
                #-cv2.imshow('3.1_frangi_inv', cl1)

                binarized = np.zeros((height, width, 3), dtype = "uint8")
                binarized = np.uint8(binarized)
                binarized = cv2.cvtColor(binarized, cv2.COLOR_BGR2GRAY)

                em_gray = cv2.cvtColor(e_im, cv2.COLOR_BGR2GRAY)

                res = cv2.bitwise_and(franghi, franghi, mask = em_gray)
                #-cv2.imshow('applied mask', res)
    
                res = np.uint8(res*255)
                res = cv2.medianBlur(res, 13)

                #https://learnopencv.com/opencv-threshold-python-cpp/
                th, binarized = cv2.threshold(res, 15, 255, cv2.THRESH_BINARY)
                #cv2.imshow('Binarized', binarized)

                skeleton = skeletonize(binarized / 255)
                skeleton = skeleton.astype(np.uint8)
                #cv2.imshow('Skeleton', skeleton * 255)

                img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
                color = np.array([30, 10, 190], dtype = np.uint8)
                img[skeleton * 255 > 0] = color
                cv2.imshow('Highlighted Veins', img)

                while(1):
                    k = cv2.waitKey(5) & 0xFF
                    if k == 27:
                        break
                
                cv2.destroyAllWindows()

                # save to disk
                cv2.imwrite(output_file, img)
                print(f'Success! File {output_file} has been written. It was file with number: {counter}')
