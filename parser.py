import numpy as np
import finger_plots as fingers
from finger_plots import cv2


image = cv2.imread('10_r_index_8.png')
fingers.plot_borders(image)

#TODO: Perspective transformation SRC: https://stackoverflow.com/questions/57207975/what-is-an-efficient-way-to-crop-out-a-slanted-box-from-image

# Set width and height of output image
W, H = 600, 200

# Define points in input image: top-left, top-right, bottom-right, bottom-left
pts0 = np.float32([[830,200],[1825,1180],[1600,1550],[320,650]])

# Define corresponding points in output image
pts1 = np.float32([[0,0],[W,0],[W,H],[0,H]])

# Get perspective transform and apply it
M = cv2.getPerspectiveTransform(pts0,pts1)
result = cv2.warpPerspective(image,M,(W,H))

# Save reult
cv2.imwrite('result.png', result)
