import os,sys
from pymongo.connection import Connection
from progressbar import ProgressBar
from osgeo import ogr
import json
from utils import create_feature_in_georegistry


def shape2mongodb(shape_path, mongodb_server, mongodb_port, mongodb_db, mongodb_collection, append, query_filter):
    """Convert a shapefile to a mongodb collection"""
    print ' Converting a shapefile to a mongodb collection '
    driver = ogr.GetDriverByName('ESRI Shapefile')
    print 'Opening the shapefile %s...' % shape_path
    ds = driver.Open(shape_path, 0)
    if ds is None:
        print 'Can not open', ds
        sys.exit(1)
    lyr = ds.GetLayer()
    totfeats = lyr.GetFeatureCount()
    lyr.SetAttributeFilter(query_filter)
    print 'Starting to load %s of %s features in shapefile %s to MongoDB...' % (lyr.GetFeatureCount(), totfeats, lyr.GetName())
    print 'Opening MongoDB connection to server %s:%i...' % (mongodb_server, mongodb_port)
    connection = Connection(mongodb_server, mongodb_port)
    print 'Getting database %s' % mongodb_db
    db = connection[mongodb_db]
    print 'Getting the collection %s' % mongodb_collection
    collection = db[mongodb_collection]
    if append == False:
        print 'Removing features from the collection...'
        collection.remove({})
    print 'Starting loading features...'
    # define the progressbar
    pbar = ProgressBar(maxval=lyr.GetFeatureCount()).start()
    k=0
    # iterate the features and access its attributes (including geometry) to store them in MongoDb
    feat = lyr.GetNextFeature()
    while feat:
        mongofeat = {}
        geom = feat.GetGeometryRef()
        mongogeom = geom.ExportToWkt()
        mongogeom = geom.ExportToJson()
        #print geom.ExportToJson()
        mongofeat['geom'] = mongogeom
        # iterate the feature's fields to get its values and store them in MongoDb
        feat_defn = lyr.GetLayerDefn()
        for i in range(feat_defn.GetFieldCount()):
            value = feat.GetField(i)
            if isinstance(value, str):
                value = unicode(value, 'latin-1')
            field = feat.GetFieldDefnRef(i)
            fieldname = field.GetName()
            mongofeat[fieldname] = value
        # insert the feature in the collection
        collection.insert(mongofeat)
        feat.Destroy()
        feat = lyr.GetNextFeature()
        k = k + 1
        pbar.update(k)
    pbar.finish()
    print '%s features loaded in MongoDb from shapefile.' % lyr.GetFeatureCount()

def extractshapes4gr(shape_path, d):
    l=[]
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.Open(shape_path, 0)
    if ds is None:
        print 'Can not open', ds
        sys.exit(1)
    lyr = ds.GetLayer()
    totfeats = lyr.GetFeatureCount()
    lyr.SetAttributeFilter('')
    print 'Starting to load %s of %s features in shapefile %s to Georegistry...' % (lyr.GetFeatureCount(), totfeats, lyr.GetName())
    pbar = ProgressBar(maxval=lyr.GetFeatureCount()).start()
    k=0
    # iterate the features and access its attributes (including geometry) to store them in MongoDb
    feat = lyr.GetNextFeature()
    while feat:
        geom = feat.GetGeometryRef()
        #mongogeom = geom.ExportToWkt()
        #mongogeom = geom.ExportToJson()
        #print geom.ExportToJson()
        g = json.loads(geom.ExportToJson())
        g['geometry_coordinates']=g['coordinates'][0]
        g['geometry_type']=g['type']
        del g['coordinates']
        del g['type']
        
        d.update(g)
        
        # iterate the feature's fields to get its values and store them in MongoDb
        feat_defn = lyr.GetLayerDefn()
        for i in range(feat_defn.GetFieldCount()):
            value = feat.GetField(i)
            if isinstance(value, str):
                value = unicode(value, 'latin-1')
            field = feat.GetFieldDefnRef(i)
            fieldname = field.GetName()
            d[fieldname] = value
        #print d
        l.append(d) 
        feat.Destroy()
        feat = lyr.GetNextFeature()
        k = k + 1
        pbar.update(k)
    pbar.finish()
    return l


def extractshapes(shape_path, wkt_or_json="JSON"):
    """
    Return a list of geometries in the shape file in either WKT or GEOJSON format
    """
    l=[]
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.Open(shape_path, 0)
    if ds is None:
        print 'Can not open', ds
        sys.exit(1)
    lyr = ds.GetLayer()
    totfeats = lyr.GetFeatureCount()
    lyr.SetAttributeFilter('')
    print 'Starting to load %s of %s features in shapefile %s...' % (lyr.GetFeatureCount(), totfeats, lyr.GetName())
    pbar = ProgressBar(maxval=lyr.GetFeatureCount()).start()
    k=0
    # iterate the features and access its attributes (including geometry) to store them in MongoDb
    feat = lyr.GetNextFeature()
    while feat:
        geom = feat.GetGeometryRef()
        #mongogeom = geom.ExportToWkt()
        #mongogeom = geom.ExportToJson()
        #print geom.ExportToJson()
        if wkt_or_json.upper()=="JSON":
            g = geom.ExportToJson()
        elif wkt_or_json.upper()=="WKT":
            g = geom.ExportToWkt()
        
        # iterate the feature's fields to get its values and store them in MongoDb
        feat_defn = lyr.GetLayerDefn()
        for i in range(feat_defn.GetFieldCount()):
            value = feat.GetField(i)
            if isinstance(value, str):
                value = unicode(value, 'latin-1')
            field = feat.GetFieldDefnRef(i)
            fieldname = field.GetName()
            d[fieldname] = value
        l.append(g) 
        feat.Destroy()
        feat = lyr.GetNextFeature()
        k = k + 1
        pbar.update(k)
    pbar.finish()
    return l


if __name__ == "__main__":
    
        try:
            filename =  sys.argv[1]
            grserver =  sys.argv[2]
            gruser   =  sys.argv[3]
            grpass   =  sys.argv[4]
            name     =  sys.argv[5]
            country_code     =  sys.argv[6]
            subdivision_code =  sys.argv[7]
            
            #fetch the geometry from the file
            
            d={'name': name,
               'classifiers': "place.locality",
               'country_code':country_code,
               'subdivision_code': subdivision_code,
               }
            
            #grab all the shapes in the file and retun a python list
            l = extractshapes4gr(filename, d)
            
            counter=0
            txfailed=0
            
            
            for i in l:
                x= create_feature_in_georegistry(i, grserver, gruser, grpass)
                #print x
                x=json.loads(x)
                if x["status"]!="200":
                    txfailed+=1
                    #print "Failed"
                counter+=1
            print "Done!  %s records processed. %s Failures." % (counter,txfailed )
            
        except:
            print "Error."
            print sys.exc_info()


