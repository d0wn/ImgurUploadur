#!/usr/bin/python
# Copyright 2009 d0wn

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os

def Install():
    sys.stdout.write("Checking for /usr/local/bin/..\n")
    if os.path.exists("/usr/local/bin/") is True:
        sys.stdout.write("Path found! Checking for /usr/local/bin/imgur..\n")
        if os.path.exists("/usr/local/bin/imgur") is True:
            sys.stdout.write("ImgurUploadur already installed!\n\n")
            sys.exit()
        elif os.path.exists("/usr/local/bin/imgur") is False:
            input = open("./imgur.py", "r")
            output = open("/usr/local/bin/imgur", "w")
            sys.stdout.write("Installing ImgurUploadur..\n")
            output.write(input.read())
            input.close
            output.close
            os.chmod("/usr/local/bin/imgur",  0755)
            sys.stdout.write("ImgurUploadur has been installed!\n")
            sys.exit()
    elif os.path.exists("/usr/local/bin/") is False:
        sys.stdout.write("Could not find /usr/local/bin/...Exiting\n")
        sys.exit()
        
def Update():
    sys.stdout.write("Checking for /usr/local/bin/..\n")
    if os.path.exists("/usr/local/bin/") is True:
        sys.stdout.write("Path found! Checking for /usr/local/bin/imgur..\n")
        if os.path.exists("/usr/local/bin/imgur") is True:
            sys.stdout.write("Deleting old version..\n")
            os.unlink("/usr/local/bin/imgur")
            input = open("./imgur.py", "r")
            output = open("/usr/local/bin/imgur", "w")
            sys.stdout.write("Installing ImgurUploadur..\n")
            output.write(input.read())
            input.close
            output.close
            os.chmod("/usr/local/bin/imgur",  0755)
            sys.stdout.write("ImgurUploadur has been installed\n")
        else: 
            sys.stdout.write("File not found! ImgurUploadur is not installed.")
            sys.exit()
    else:
        sys.stdout.write("Path not found! /usr/local/bin/..\n")
        sys.exit()

def Uninstall():
    sys.stdout.write("Checking for /usr/local/bin/..\n")
    if os.path.exists("/usr/local/bin/") is True:
        sys.stdout.write("Path found! Checking for /usr/local/bin/imgur..\n")
        if os.path.exists("/usr/local/bin/imgur") is True:
            sys.stdout.write("Uninstalling version..\n")
            os.unlink("/usr/local/bin/imgur")
            if os.path.exists("/usr/local/bin/imgur") is True:
                sys.stdout.write("Something messed up..\n")
                sys.exit()
            else: 
                sys.stdout.write("ImgurUploadur uninstalled..\n")
                sys.exit()
    
if __name__ == "__main__":
    print "\n\nWelcome to the ImgurUploadur simple installer. This is just currently the only thing I will be using to install it during beta.\n\n"
    
    menu = input("Would you like to:\n\n" \
                 "\t[1] Install ImgurUploadur\n" \
                 "\t[2] Update ImgurUploadur\n" \
                 "\t[3] Uninstall ImgurUploadur\n" \
                 "\t[4] Exit\n" \
                 "Input> ")
                 
    if menu == 1: Install()
    elif menu == 2: Update()
    elif menu == 3: Uninstall()
    elif menu == 4: sys.exit()
    else:
        sys.stdout.write("Only accepts input 1-4\n")
        sys.exit()
