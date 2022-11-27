import numpy as np
import cv2
from matplotlib import pyplot as plt # potom zmazat
import sys

# it shows image with given points if it is True
isTesting = False


# function which parse photo of finger to corresponding parts
def parse(image_name, path_to_save, path_to_load, counter):
    image = cv2.imread(path_to_load + "/" + image_name)

    #TODO: Perspective transformation SRC: https://stackoverflow.com/questions/57207975/what-is-an-efficient-way-to-crop-out-a-slanted-box-from-image

    # Set width and height of output image
    W, H = 600, 200

    # Define points in input image: top-left, top-right, bottom-right, bottom-left
    points_matrix = np.float32([
        [[830,200],[1825,1180],[1600,1550],[320,650]],  # red
        [[25,2650], [1290,2025],[1500,2150],[550,2990]], # orange
        [[25,1815],[1290,1775],[1510,1930],[25,2550]],  # cyan
        [[25,1200],[1400,1500],[1510,1750],[25,1835]],  # yellow
        [[2500,25],[2230,1330],[1905,1330],[1500,25]],  # lime
        [[3685,780],[2500,1530],[2270,1250],[2875,25]], # salmon
        [[4050,1720],[2650,1720],[2750,1450],[4050,1200]], # violet
        [[4050,2400],[2650,1930],[2900,1750],[4050,1800]], # navy
        [[3700,2990],[2650,2150],[2750,2000],[4050,2650]], # blue
        [[1400,2990],[1800,2000],[2300,2000],[2600,2990]], # green
        ])
    
    # just description of finger position on photo
    position = 1

    for i in points_matrix:
        # Define corresponding points in input image
        pts0 = np.float32([i[0], i[1], i[2], i[3]])
        
        # Define corresponding points in output image
        pts1 = np.float32([[0,0],[W,0],[W,H],[0,H]])

        # Get perspective transform and apply it
        M = cv2.getPerspectiveTransform(pts0,pts1)
        result = cv2.warpPerspective(image,M,(W,H))

        # Save reult
        cv2.imwrite(path_to_save + "position" + str(position) + "_" + image_name, result)
        print(f'Success! File {str(path_to_save + "position" + str(position) + "_" + image_name)} has been written. It was file with number: {counter}')
        counter += 1
        position += 1
    
    # Show points on image
    if isTesting == True:
        plotPointsForTest(points_matrix, image) # just test if points are correct 
    
    return counter

# function to plot points which are used for perspective transformation
def plotPointsForTest(points_matrix, image):
    colour_matrix = ["red", "orange", "cyan", "yellow", "lime", "salmon", "violet", "navy", "blue", "green"]

    counter = 0
    for i in points_matrix:
        for j in i:
            plt.plot(j[0], j[1], marker='+', color=colour_matrix[counter])
        
        counter += 1

    plt.imshow(image)
    plt.show()

