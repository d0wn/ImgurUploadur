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

import re
import os.path
import sys

def Usage():
    usage = "\n\tImgurUploadur v0.1b by d0wn" \
                  "\n\thttp://github.com/d0wn/ImgurUploadur/\n" \
                  "\nUsage: ./imgur.py [Local file | URL]\n" \
                  "or       imgur  [Local file | URL]\n\n"
    
    return usage

def pUpload(pLoc):
    # Function to parse the API's XML and figure out if the image is a URL or local file 
    # talks to cUpload, the curl uploader
    # Depends on elementtree

    if re.search("(http|https):\/\/",  pLoc): isURL = 1
    else: isURL = 0
    
    xml = cUpload(pLoc,  isURL)
    element = ET.XML(xml)
    
    if element.attrib['stat'] == "ok":
        # parses needed text into a dict, and returns it
        element_array = { "image_hash": element.find("image_hash").text, 
                                     "delete_hash": element.find("delete_hash").text, 
                                     "original_image": element.find("original_image").text, 
                                     "large_thumbnail": element.find("large_thumbnail").text, 
                                     "small_thumbnail": element.find("small_thumbnail").text, 
                                     "imgur_page": element.find("imgur_page").text, 
                                     "delete_page": element.find("delete_page").text }
        return element_array
    elif element.attrib['stat'] == "fail": 
        return "Error" # Vague for now

def cUpload(imgLoc, isURL): 
    # Function to process the HTTP POST and GET requests.
    # Depends on pycurl module
    from cStringIO import StringIO

    cPost = pycurl.Curl()
    
    values = [("key", "c4eb08d39a32e5a71c3df7225f137f06221476db")]
    
    
    if isURL == 0: 
        if os.path.exists(imgLoc): # Checks if the file exists
            values.append(("image", (cPost.FORM_FILE,  imgLoc)))
    if isURL == 1: values.append(("image", imgLoc))
    
    cPost.setopt(cPost.POST, 1)
    cPost.setopt(cPost.VERBOSE,  0)
    cPost.setopt(cPost.URL, "http://imgur.com/api/upload/")
    cPost.setopt(cPost.HTTPPOST, values)
    buffer = StringIO()
    cPost.setopt(cPost.WRITEFUNCTION,  buffer.write)
    cPost.perform()
    
    return buffer.getvalue()
    
if __name__ == "__main__":
    # Checks for all dependencies
    try:
        from elementtree import ElementTree as ET
    except ImportError:
        print "You do not have the elementtree module. Please visit http://effbot.org/downloads/#elementtree and download/install elementtree-1.2.6-20050316.tar.gz."
        sys.exit()
    try:
        import pycurl
    except ImportError:
        print "You do not have the pycurl module. Please visit http://pycurl.sourceforge.net/."
        sys.exit()

    if len(sys.argv) == 1:
        print Usage()
        sys.exit()
    parse = pUpload(sys.argv[1])
    print parse['original_image'] # prints link
    print parse['delete_page']      # prints deletion link


