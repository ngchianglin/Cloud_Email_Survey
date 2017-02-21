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
#
# This script makes use of dnspython module. 
# http://www.dnspython.org/
# Dnspython needs to be installed before using this. 
#
# Simple python app to read in a csv text file
# with each line having the format
# <company name>;<domain1>,<domain2>,<domain3>,.....
# and query the MX record for each domain
#
# Ng Chiang Lin
# Feb 2017
#

import dns.resolver
import time



#
# Function to read in the csv and format it into a lookup list containing
# other lists of name value pair, consisting of a company name and a domain. 
# Eg.
#
# [["Company name1","domain1"],["Company name1", "domain2"], ....] 
#

def readcsvfile(csv_filename):
    lookuplist=[]

    fcsv = open(csv_filename, "r")
    line = fcsv.readline()

    for line in fcsv:
       line = line.strip()
       namedomains = line.split(";")
       namedomains[0] = namedomains[0].strip().lower()
       domains = namedomains[1].split(",")
       for d in range(len(domains)):
           domains[d] = domains[d].strip().lower()      
           lookup_name_pair = [namedomains[0], domains[d]]
           lookuplist.append(lookup_name_pair)

    fcsv.close()
    return lookuplist



#
# Do a MX lookup for each of the name value pair in the lookup list
# and output the result in the format
# 
# Company Name1;domain1;MX1
# Company Name1;domain1;MX2 
# ....
#
# If there is no MX for a domain, "NOMX" will be used in place of the actual MX record. 
#
def lookupMX(lookuplist):
   
   for i in range(len(lookuplist)):
     
      try:
         answers = None
         answers = dns.resolver.query(lookuplist[i][1], 'MX')
      except dns.exception.DNSException:
         #Do nothing here if there is no MX
         pass

      if answers == None:
         #No MX record for domain
         print(lookuplist[i][0], ";" , lookuplist[i][1], ";", "NOMX", sep="")
      else: 
          for rdata in answers:
             print(lookuplist[i][0], ";" , lookuplist[i][1], ";" , rdata.exchange, sep="")
        
      #Sleep for 2 seconds to avoid excessive DNS query
      time.sleep(2)

   return





if __name__ == "__main__":
      lookuplist = readcsvfile("cloudemail-format1.csv")    
      lookupMX(lookuplist)



