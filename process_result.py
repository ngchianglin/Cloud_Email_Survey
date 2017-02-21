#!/usr/bin/python3
#
#***************************************************************************
#  MIT License
# 
# Copyright (c) 2017 Ng Chiang Lin
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
# ***************************************************************************
#
# Simple python app to read in a text file
# with each line having the format
# <company name>;<domain1>;<mail exchanger>
#
# and these results into a 
# dictionary containing 
# <company name> and its unique <mail exchanger domain>
#
# Ng Chiang Lin
# Feb 2017


TLDS={"sg":True, 
      "in":True,
      "au":True,
      "my":True,
      "hk":True,
      "vn":True,
      "uk":True
    }


#
# Takes a mx hostname as argument
# Returns the domain of a mail exchanger
#
def getMxDomain(mxhostname):
    mxparts = mxhostname.split(".")
    length = len(mxparts)
    tld = mxparts[length -2]
    if tld in TLDS :
        domain = mxparts[length -4] + "." + mxparts[length -3] + "." + mxparts[length -2]
    else:
         domain = mxparts[length -3] + "." + mxparts[length -2]
    return domain.lower()


if __name__ == "__main__":

    f = open("results2.txt", "r")
    company = None
    mxlist = None
    namemx = {}
    for line in f:
        line = line.strip()
        part = line.split(";")
        if part[0] != company :
            #new company name, create new list and add it to dictionary
            company = part[0]
            mxlist = []
            namemx[company] = mxlist
            if part[2] != "NOMX" :
               mxdomain = getMxDomain(part[2])       
               mxlist.append(mxdomain)

        else:
            #existing company, add to existing list
            if part[2] != "NOMX" :
               mxdomain = getMxDomain(part[2])
               mxlist.append(mxdomain)             

    f.close()

    
    for k in namemx:
       mxlist = namemx[k]
       namemx[k] = list(set(mxlist)) #Get the unique mx domains
       for unique in namemx[k]:
           print(k, ";" , unique, sep="")       

    


