# BIO Project
# Authors:  Radoslav Páleník <xpalen05@stud.fit.vutbr.cz>, Jozef Čabala <xcabal07@stud.fit.vutbr.cz>, Jana Gregorová <xgrego20@stud.fit.vutbr.cz>
# Name: Finger blood vessel detection from multiple viewpoints
# Date 2022-12-04
import cv2
import numpy as np

def getBestContrast(path):
    
    # read image
    img = cv2.imread(path)

    # convert to LAB color space
    lab = cv2.cvtColor(img,cv2.COLOR_BGR2LAB)

    # separate channels
    L,A,B=cv2.split(lab)

    # compute minimum and maximum in 5x5 region using erode and dilate
    kernel = np.ones((5,5),np.uint8)
    min = cv2.erode(L,kernel,iterations = 1)
    max = cv2.dilate(L,kernel,iterations = 1)

    # convert min and max to floats
    min = min.astype(np.float64) 
    max = max.astype(np.float64) 

    average_contrast = 0

    # compute local contrast
    if ((max + min).all() is not None) and ((max + min).all() != 0):
        contrast = (max-min)/(max+min)
        #print(f'path: {path} max: {max} min: {min} contrast: {contrast}')

        # get average across whole image
        average_contrast = 100*np.mean(contrast)

    return average_contrast
