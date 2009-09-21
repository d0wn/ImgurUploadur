#!/usr/bin/python

import pycurl
import re
import os.path
from cStringIO import StringIO

def pUpload(pLoc):
    # Function to parse the API's XML and figure out if the image is a URL or local file 
    # talks to cUpload, the curl uploader
    if re.search("http:\/\/",  pLoc):
        return cUpload(pLoc,  1)
    else: 
        return cUpload(imgLoc,  0)

def cUpload(imgLoc, isURL): 
    cPost = pycurl.Curl()
    
    if isURL == 1:
        # if os.path.isfile("/tmp/imgurTmpImg") == true: os.unlink("/tmp/imgurTmpImg")
        tmpFile = "/tmp/imgurTmpImg"
        tmpFileLoc = open(tmpFile,  "w")
        cGet  = pycurl.Curl()
        cGet.setopt(cGet.URL,  imgLoc)
        cGet.setopt(cGet.WRITEDATA,  tmpFileLoc)
        cGet.setopt(cGet.VERBOSE,  1)
        #cGet.perform()
      #  output = open(tmpFileLoc,  "w")
      # output.write(buffer.getvalue)
        
        values = [ ("key", "c4eb08d39a32e5a71c3df7225f137f06221476db"),  ("image", (cPost.FORM_FILE,  tmpFile)) ]
        cGet.close
        #output.close
        tmpFileLoc.close
        
    
    if isURL == 0: values = [ ("key", "c4eb08d39a32e5a71c3df7225f137f06221476db"),  ("image", (cPost.FORM_FILE,  imgLoc)) ]
    cPost.setopt(cPost.POST, 1)
    cPost.setopt(cPost.VERBOSE,  0)
    cPost.setopt(cPost.URL, "http://imgur.com/api/upload/")
    cPost.setopt(cPost.HTTPPOST, values)
    buffer = StringIO()
    cPost.setopt(cPost.WRITEFUNCTION,  buffer.write)
    # if os.path.isfile("/tmp/imgurTmpImg") == true: os.unlink("/tmp/imgurTmpImg")
    cPost.perform()
    return buffer.getvalue()
    

cUpload("./smiley2.png",  0)
