#!/usr/bin/python

#just a little info before any of you try using my code, i have no idea what i'm doing, and there WILL be bugs

import pycurl
import re
import os.path
import sys
from elementtree import ElementTree as ET
from cStringIO import StringIO

def pUpload(pLoc):
    # Function to parse the API's XML and figure out if the image is a URL or local file 
    # talks to cUpload, the curl uploader
    if re.search("(http|https):\/\/",  pLoc): isURL = 1
    else: isURL = 0
    
    xml = cUpload(pLoc,  isURL)
    element = ET.XML(xml)
    if element.attrib['stat'] == "ok":
        return element.find("original_image").text
    elif element.attrib['stat'] == "fail": 
        return "Error" # Vague for now. Still have to parse the error codes
        

def cUpload(imgLoc, isURL): 
    # Function to process the HTTP POST and GET requests.
    # Depends on pycurl module
    cPost = pycurl.Curl()
    
    if isURL == 1:
        tmpFile = "/tmp/imgurTmpImg"
        if os.path.isfile(tmpFile) is True: os.unlink(tmpFile)
        tmpFileLoc = open(tmpFile,  "w")
        cGet  = pycurl.Curl()
        cGet.setopt(cGet.URL,  imgLoc)
        cGet.setopt(cGet.WRITEDATA,  tmpFileLoc)
        cGet.setopt(cGet.VERBOSE,  0)
        cGet.perform()
        
        values = [ ("key", "c4eb08d39a32e5a71c3df7225f137f06221476db"),  ("image", (cPost.FORM_FILE,  tmpFile)) ]
        cGet.close
        tmpFileLoc.close
        
    
    if isURL == 0: values = [ ("key", "c4eb08d39a32e5a71c3df7225f137f06221476db"),  ("image", (cPost.FORM_FILE,  imgLoc)) ]
    cPost.setopt(cPost.POST, 1)
    cPost.setopt(cPost.VERBOSE,  0)
    cPost.setopt(cPost.URL, "http://imgur.com/api/upload/")
    cPost.setopt(cPost.HTTPPOST, values)
    buffer = StringIO()
    cPost.setopt(cPost.WRITEFUNCTION,  buffer.write)
    cPost.perform()
    return buffer.getvalue()
    
if __name__ == "__main__":
        print pUpload(sys.argv[1])


