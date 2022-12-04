# BIO Project
# Authors:  Radoslav Páleník <xpalen05@stud.fit.vutbr.cz>, Jozef Čabala <xcabal07@stud.fit.vutbr.cz>, Jana Gregorová <xgrego20@stud.fit.vutbr.cz>
# Name: Finger blood vessel detection from multiple viewpoints
# Date 2022-12-04
import os
import sys
import shutil

def ifDirNotExistCreate(name):
    if not os.path.isdir(name):
        os.makedirs(name)
    else:
        isDirExistDelete(name)
        os.makedirs(name)

def ifDirNotExistExit(name):
    if not os.path.isdir(name):
            print(f'{name} does not exist! Run program again and enter correct name of directory')
            sys.exit(0)

def isDirEndingOnCorrectSymbol(name):
    if not name[len(name)-1].isalnum():
            print(f'{name} is ending on slash or backslash! Run program again and enter correct name of directory e.g data')
            sys.exit(0)

def isDirExistDelete(name):
    if os.path.exists(name):
        user_input = input(f'{name} is existing. Delete it?[y/n]: ')

        if user_input.lower() == 'y':
            shutil.rmtree(name)
        elif user_input.lower() == 'n':
            print("Run application again and enter another name")
            sys.exit(0)
        else:
            print("Run application again and enter y or n")
            sys.exit(0)
        