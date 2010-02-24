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
    usage = "\n\tImgurUploadur v0.2b by d0wn" \
                  "\n\thttp://github.com/d0wn/ImgurUploadur/\n\n" \

    
    print usage

def getElementValue(nodelist):
    """ From http://docs.python.org/library/xml.dom.minidom.html#dom-example """
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

def pUpload(pLoc):
    # Function to parse the API's XML and figure out if the image is a URL or local file 
    # talks to cUpload, the curl uploader
    # Depends on xml.dom.minidom

    if re.search("(http|https):\/\/",  pLoc): isURL = 1
    else: isURL = 0
    
    xml = cUpload(pLoc,  isURL)
    
    element = parseString(xml)
    
    attrib = element.getElementsByTagName("rsp")[0] # <rsp>
    
    if attrib.attributes.keys()[0] == u"stat": # Checks if the "stat" attribute exists on <rsp>
        if attrib.attributes["stat"].value == u"ok": # <rsp stat="ok">? Checks if the "stat" attribute's value is "ok"
            element_dict = {"image_hash": getElementValue(element.getElementsByTagName("image_hash")[0].childNodes),  # <image_hash>value</image_hash>
                            "delete_hash": getElementValue(element.getElementsByTagName("delete_hash")[0].childNodes), # etc
                            "original_image": getElementValue(element.getElementsByTagName("original_image")[0].childNodes), 
                            "large_thumbnail": getElementValue(element.getElementsByTagName("large_thumbnail")[0].childNodes), 
                            "small_thumbnail": getElementValue(element.getElementsByTagName("small_thumbnail")[0].childNodes), 
                            "imgur_page": getElementValue(element.getElementsByTagName("imgur_page")[0].childNodes),
                            "delete_page": getElementValue(element.getElementsByTagName("delete_page")[0].childNodes)}
            return element_dict
        if attrib.attributes["stat"].value == u"fail":
            element_dict = {"error_code": getElementValue(element.getElementsByTagName("error_code")[0].childNodes), 
                            "error_msg": getElementValue(element.getElementsByTagName("error_msg")[0].childNodes)}
            return element_dict

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
    cPost.setopt(cPost.URL, "http://imgur.com/api/upload.xml")
    cPost.setopt(cPost.HTTPPOST, values)
    buffer = StringIO()
    cPost.setopt(cPost.WRITEFUNCTION,  buffer.write)
    cPost.perform()
    
    return buffer.getvalue()
 
def main():
    option = optparse.OptionParser(usage="%prog [options] [FILE | URL]",  version="ImgurUploadur 0.2b")
    option.add_option("-q", "--quiet",  action="store_true", 
                      dest="quiet",  help="Print only the image URL to stdout")
    (options,  args) = option.parse_args()
    if len(args) == 0:
        Usage()
        option.print_help()
        sys.exit()

    parse = pUpload(args[0]) 
    
    try: # Check if there were any errors
        print "Error %s: %s" % (parse["error_code"],  parse["error_msg"])
    except KeyError: # Output image link and delete page if no errors are found
        if options.quiet is True: # If -q or --quiet is passed, then output only the image link
            output = (parse["original_image"])
            sys.stdout.write("%s\n" % (output))
        else:
            output = (parse["original_image"],  parse["delete_page"])
            sys.stdout.write("%s\n%s\n" % (output))
            
    
if __name__ == "__main__":
    # Checks for all dependencies before starting
    try:
        from xml.dom.minidom import parse,  parseString
    except ImportError:
        print "Could not import xml.dom.minidom module"
        sys.exit()
    try:
        import pycurl
    except ImportError:
        print "You do not have the pycurl module. Please visit http://pycurl.sourceforge.net/."
        sys.exit()
    try:
        import optparse
    except ImportError:
        print "Could not import optparse module."
        sys.exit()

    main() # Start main()
