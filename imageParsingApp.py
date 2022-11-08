import os
import argparse
from parser import parse as p
import sys

# function which find out if dir exists, if not create dir
def ifDirNotExistCreate(name):
    if not os.path.isdir(name):
        os.makedirs(name)
        return False
    
    return True

parser = argparse.ArgumentParser()
 
# This is to get the directory that the program
# is currently running in.
dir_path = os.path.dirname(os.path.realpath(__file__))

# adding argument for setting path to data
parser.add_argument("-data", "--data", help="Name of data directory (directory where are photos of fingers)", type=str)
args = parser.parse_args()

data_directory_name = args.data

# just check if flag was set
if(data_directory_name == None):
    print("You do not enter name of data directory. Directory must be in directory where is .py file. Use flag --data<name of directory> or -data <name of directory>")
    sys.exit(0)
elif not os.path.isdir(data_directory_name):
    print("Directory with this name does not exist! Run program again and enter correct name")
    sys.exit(0)

data_directory_path = dir_path + "/" + data_directory_name 
data_directory_name_after_splitting = data_directory_name + "-after-splitting"

# create dir for saving each angel of finger photos
ifDirNotExistCreate(data_directory_name_after_splitting)

# splitting finger photos into corresponding parts and saving them to corresponding dir (its copy structure of original directory where were photos of fingers)
for root, dirs, files in os.walk(dir_path + "/" + str(data_directory_name)):
    for dir in dirs: 
        ifDirNotExistCreate(data_directory_name_after_splitting + root[len(data_directory_path):] + "/" + dir)

    for file in files:
        p(file, data_directory_name_after_splitting + root[len(data_directory_path):] + "/", root)