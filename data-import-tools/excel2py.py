#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
import slugify
import xlrd
import sys
from utils import create_feature_in_georegistry
import json
GR_SERVER="http://127.0.0.1:8000"
GR_USER="alan"
GR_PASS="pass"
classifiers="place.locality"

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
    txfailed=0
    for i in data:
        #format the geometry_coordinates
        print "Uploading record #%s" % (counter)
        if i.has_key('name'):
            i['name']="%s" %i['name']
            i['name']=slugify.slugify(i['name'])
            print i['name']
        if i.has_key('geometry_coordinates'):
            splitgeo=i['geometry_coordinates'].split(" ")
            i['geometry_coordinates']="[ %s, %s ]" %  (splitgeo[0], splitgeo[1])
        elif i.has_key('lat') and i.has_key('lon'):
            i['geometry_coordinates']="[ %s, %s ]" %  (i['lat'], i['lon'])
            del i['lat']
            del i['lon']
        if not i.has_key('geometry_type'):
            i['geometry_type']="Point"
            
        if not i.has_key('subdivision_code'):
            i['subdivision_code']="XX"
        
        if not i.has_key('classifiers'):
            i['classifiers']=classifiers  
        
        x= create_feature_in_georegistry(i, GR_SERVER, GR_USER, GR_PASS)
        #print x
        x=json.loads(x)
        if x["status"]!="200":
          txfailed+=1
          print "Failed"
        counter+=1
    print "Done! %s records processed. %s Failures." % (counter, txfailed )
    
if __name__ == "__main__":
    
        try:
            filename =  sys.argv[1]
            excel2py(filename)
        except:
            print "Error."
            print sys.exc_info()
