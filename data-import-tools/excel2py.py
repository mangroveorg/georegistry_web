#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import xlrd
import sys
from utils import create_feature_in_georegistry

GR_SERVER="http://georegistry_web.org"
GR_USER="aviars"
GR_PASS="pass"

def excel2py(filename):
    book = xlrd.open_workbook(filename) #open our xls file,
    sheet=book.sheets()[0]
    r = sheet.row(0)
    r= sheet.row_values(0)
    
    data = []
    #
    for i in xrange(sheet.nrows):
        #
        if i==0:
            k=sheet.row_values(i)
        else:
            combo=zip(k, sheet.row_values(i))
            combo=dict(combo)
            data.append(combo)
            #data.append(sheet.row_values(i)) #drop all the values in the rows into data
            #print len(sheet.row_values(i))
            
            
    #now load our queryset-like object into the GR
    counter=0
    for i in data:
        #format the geometry_coordinates
        print "Uploading record #%s" % (counter)
        splitgeo=i['geometry_coordinates'].split(" ")
        i['geometry_coordinates']="[ %s, %s ]" %  (splitgeo[0],splitgeo[1])
        x= create_feature_in_georegistry(i, GR_SERVER, GR_USER, GR_PASS)
        print x
        counter+=1
    print "Done!  %s records processed." % (counter)
    
if __name__ == "__main__":
    
        try:
            filename =  sys.argv[1]
            excel2py(filename)
        except:
            print "Error."
            print sys.exc_info()