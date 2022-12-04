# BIO Project
# Authors:  Radoslav Páleník <xpalen05@stud.fit.vutbr.cz>, Jozef Čabala <xcabal07@stud.fit.vutbr.cz>, Jana Gregorová <xgrego20@stud.fit.vutbr.cz>
# Name: Finger blood vessel detection from multiple viewpoints
# Date 2022-12-04
from parser import parse as p
from contrast import getBestContrast as contrast
import os
import fnmatch
import helper

def start(dir_path, data_directory_name, output_directory_name):
    data_directory_path = dir_path + "/" + data_directory_name 

    # create dir for saving each angel of finger photos
    helper.ifDirNotExistCreate(output_directory_name)

    counter = 1

    # splitting finger photos into corresponding parts and saving them to corresponding dir (its copy structure of original directory where were photos of fingers)
    for root, dirs, files in os.walk(dir_path + "/" + str(data_directory_name)):
        for dir in dirs: 
            helper.ifDirNotExistCreate(output_directory_name + root[len(data_directory_path):] + "/" + dir)
        max = 0
        fileName = ""
        for file in files:
            if fnmatch.fnmatch(file, '*.png'):
                result = contrast((root + "/" + file))
                # print(f'max: {max} result: {result} fileNameMAX: {fileName} fileName: {str(root + "/" + file)}') just debug
                if result > max:
                    max = result
                    fileName = file

        if fileName != "":
            counter = p(fileName, output_directory_name + root[len(data_directory_path):] + "/", root, counter)
            