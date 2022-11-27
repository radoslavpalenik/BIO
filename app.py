import sys
import os
import argparse
import helper
import dataPreparation
import veinsExtraction

parser = argparse.ArgumentParser()
 
# This is to get the directory that the program
# is currently running in.
dir_path = os.path.dirname(os.path.realpath(__file__))

# adding argument for setting data preparing, value of this argument iis path to  data directory
parser.add_argument("-dataInit", "--dataInit", help="Argument for data preparation. Value of argument is name of data directory (directory where are photos of fingers)", type=str)

# adding argument for veins extraction
parser.add_argument("-veinsExtraction", "--veinsExtraction", help="Argument for veins extraction", type=str)

# adding argument for output directory
parser.add_argument("-output", "--output", help="Argument for name of output directory", type=str)

# arg0 is python and arg1 is app.py
print("BIO Zadanie X: ")
print("Usage: \npython app.py -dataInit <path to data directory>\npython app.py -veinsExtraction <path to data prepared for veins extraction")
print("-----------------------------------------------------------------------------")

if len(sys.argv) != 5:
    print("Set --dataInit <directory name> or --veinsExtraction <directory name> and --output <directory name> ! Run application again")
else:
    args = parser.parse_args()
    data_directory_name = args.dataInit if args.dataInit is not None else args.veinsExtraction 
    output_directory_name = args.output

    helper.ifDirNotExistExit(data_directory_name)
    helper.isDirEndingOnCorrectSymbol(data_directory_name)
    helper.isDirEndingOnCorrectSymbol(output_directory_name)

    if args.dataInit is not None : 
        data_directory_name = args.dataInit
        print("Start of data preparation")
        dataPreparation.start(dir_path, data_directory_name, output_directory_name)
        print("End of data preparation")

    if args.veinsExtraction is not None: 
        data_directory_name = args.veinsExtraction
        print("Start of veins extraction")
        veinsExtraction.start(dir_path, data_directory_name, output_directory_name)
        print("End of veins extraction")