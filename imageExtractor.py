# BIO Project
# Authors:  Radoslav Páleník <xpalen05@stud.fit.vutbr.cz>, Jozef Čabala <xcabal07@stud.fit.vutbr.cz>, Jana Gregorová <xgrego20@stud.fit.vutbr.cz>
# Name: Finger blood vessel detection from multiple viewpoints
# Date 2022-12-04
import cv2
import sys
import os
import helper
import fnmatch
import numpy as np
from matplotlib import pyplot as plt
from skimage.filters import frangi, hessian
from skimage.morphology import skeletonize

def image_preparator(img):
    
    height, width = img.shape[:2]

    # Applying CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(img)


    #Canny filter
    img_canny = cv2.medianBlur(cl, 5)
    med_val = np.median(img_canny)
    lower = int(max(0 ,0.5*med_val))
    upper = int(min(255,1*med_val))

    img_canny = cv2.Canny(img_canny, lower, upper)

    return img_canny

def mask_constructor(img_canny, height, width):
    
    contours, hierarchy = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #Erases minor artifacts in image 
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if h<50 and w<50: 
            cv2.fillConvexPoly(img_canny,contour,0) 

    #Connects nearby edges with closing operation
    closing = cv2.morphologyEx(img_canny, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (150,20)));

    #Dilates finger lines to connect perimeter walls
    dil_matrix = np.ones((2,30), np.uint8) 
    d_im = cv2.dilate(closing, dil_matrix, iterations=3)


    #Gets contours of perimeter walls
    contours, hierarchy = cv2.findContours(d_im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contour_area = []

    #Image contains one global contour(perimeter wall)
    if len(contours) == 1:
        cnt = contours[0]
       
        extTop = tuple(cnt[cnt[:, :, 1].argmin()][0])
        extBot = tuple(cnt[cnt[:, :, 1].argmax()][0])

        middle =  (extBot[1] - extTop[1])/2 + extTop[1]
        mid_left = (0,int(middle))
        mid_right = (599,int(middle))
        cv2.line(d_im, mid_left,mid_right , (0,0,0), 4)
 
        
        contours, hierarchy = cv2.findContours(d_im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for c in contours:
        contour_area.append((cv2.contourArea(c), c))

    contour_area = sorted(contour_area, key=lambda x:x[0], reverse=True)
    
    mask = np.zeros((height, width, 3), dtype = "uint8")

    coords = np.vstack([contour_area[0][1], contour_area[1][1]])

    cv2.fillPoly(mask, [coords], (255, 255, 255))


    #Erodes perimeter walls to make finger mask more accurate
    er_matrix = np.ones((1,10), np.uint8)
    e_im = cv2.erode(mask, er_matrix, iterations=2) 
    e_im = cv2.rectangle(e_im, (0,0), (600,200), (0,0,0), 2)

    
    em_gray = cv2.cvtColor(e_im, cv2.COLOR_BGR2GRAY)

    contours, hierarchy = cv2.findContours(em_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contour_area = []



    for c in contours:
        contour_area.append((cv2.contourArea(c), c))

    #Finds extremes of contours to get whole finger perimeter
    c = contour_area[0][1]
    bot_left_ext = tuple(c[c[:, :, 0].argmin()][0])
    bot_right_ext = tuple(c[c[:, :, 0].argmax()][0])

    c = contour_area[1][1]
    top_left_ext = tuple(c[c[:, :, 0].argmin()][0])
    top_right_ext = tuple(c[c[:, :, 0].argmax()][0])
    
    #Creates perimeter in the image

    cv2.line(e_im, top_left_ext, bot_left_ext, (255,255,255), 2)
    cv2.line(e_im,top_right_ext, bot_right_ext, (255,255,255), 2)



    #Creates Mask

    if bot_left_ext[0] > 150:   
        cv2.line(e_im, (20, bot_left_ext[1]), bot_left_ext,(255,255,255), 2 )
        bot_left_ext = ((20, bot_left_ext[1]))
    if top_left_ext[0] > 150:
        cv2.line(e_im, (20, top_left_ext[1]), top_left_ext,(255,255,255), 2 )
        top_left_ext = (20, top_left_ext[1])
    cv2.line(e_im, top_left_ext, bot_left_ext, (255,255,255), 2)
    

    if bot_right_ext[0] < 400:
        cv2.line(e_im, bot_right_ext, (580, bot_right_ext[1]), (255,255,255), 2 )
        bot_right_ext =(580, bot_right_ext[1])
    if top_right_ext[0] < 400:
        cv2.line(e_im, top_right_ext, ( 580, top_right_ext[1]), (255,255,255), 2 )
        top_right_ext = ( 580, top_right_ext[1])
    cv2.line(e_im,top_right_ext, bot_right_ext, (255,255,255), 2)

    em_gray = cv2.cvtColor(e_im, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(em_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    cv2.drawContours(e_im, contours, -1, (255,255,255), thickness=cv2.FILLED)
    


    #Erodes perimeter walls to make finger mask more accurate
    er_matrix = np.ones((5,2), np.uint8)
    e_im = cv2.erode(e_im, er_matrix, iterations=2) 


    return e_im

def vein_extractor(img, e_im, height, width):
    
    # blur image to reduce noise
    # equalize the histogram to improve contrast
    img_eq = cv2.equalizeHist(img)

    # create Contrast Limited Adaptive Histogram Equalization
    clahe = cv2.createCLAHE(clipLimit=9.0, tileGridSize=(10, 10))
    cl1 = clahe.apply(img_eq)

    img_blur = cv2.bilateralFilter(cl1, 9, 75, 75)
    
    
    cl1 = cl1.max()-cl1
    cl1 = cl1.astype(float)
    cl1 = np.float32(cl1)
    
    cl1 = frangi(cl1, black_ridges=False)
    franghi = cl1
    

    binarized = np.zeros((height, width, 3), dtype = "uint8")
    binarized = np.uint8(binarized)
    binarized = cv2.cvtColor(binarized, cv2.COLOR_BGR2GRAY)

    em_gray = cv2.cvtColor(e_im, cv2.COLOR_BGR2GRAY)

    res = cv2.bitwise_and(franghi, franghi, mask = em_gray)


    res = np.uint8(res*255)
    res = cv2.medianBlur(res, 13)

    th, binarized = cv2.threshold(res, 15, 255, cv2.THRESH_BINARY)


    skeleton = skeletonize(binarized / 255)
    skeleton = skeleton.astype(np.uint8)
  

    img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    color = np.array([30, 10, 190], dtype = np.uint8)
    img[skeleton * 255 > 0] = color
    

    return img

if __name__ == '__main__':
    if len(sys.argv) == 2:
        file = sys.argv[1]
   
    if fnmatch.fnmatch(file, '*.png'):
            
            output_file = file[:-4] + "_veins_extractions.bmp" 
            
            # load images
            input_image = cv2.imread(file,0)

            img_canny = image_preparator(input_image)
            height, width = img_canny.shape[:2]

            e_im = mask_constructor(img_canny, height, width);
        
            img = vein_extractor(input_image, e_im, height, width)
            
            # save to disk
            cv2.imwrite(output_file, img)
            print(f'Success! File {output_file} has been written.')
    else:
        print("Wrong image format inserted")
    
