#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

try:
    import json
except ImportError:
    import simplejson as json

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from utils import query_georegistry
import urllib

    
def render_point(request, feature_id):
    """
        Plot a point
    """
    URL="api/1.0/feature/%s.json" % (feature_id)
    r= query_georegistry(URL)
    d=json.loads(r)
    if d['status']==200:
        results= d['features']
        latlon=results[0]['geometry']['coordinates']
        geomtype=results[0]['geometry']['type']
        lat=latlon[0]
        lon=latlon[1]
        properties=results[0]['properties']
        
        proplist=[]
        property_type=properties['feature_type']
        for k,v in properties.items():
            i="%s : %s" % (k,v)
            proplist.append(i)        
    else:
        jsonstr = json.dumps(d, indent=4)	
        return HttpResponse(jsonstr, status=d['status'],
                            mimetype='application/json')
    return render_to_response("point.html", {'lat': lat,
                                            'lon': lon,
                                            'proplist': proplist,
                                            'property_type': property_type
                                                   },
                              context_instance = RequestContext(request),)
    
def render_points(request, kwargs):
    """
        Plot multiple points based on a kwarg dict
    """
    data = urllib.urlencode(kwargs) 
    URL="api/1.0/features/search?%s" % (data)
    r= query_georegistry(URL)
    d=json.loads(r)
    if d['status']==200:
        
        pointslist=[]
        detaillist=[]
        for i in d['features']:
            c=0
            pointsitems=[]
            geomtype=i['geometry']['type']
            if geomtype=="Point": 
                formatted_properties=""
                latlon=i['geometry']['coordinates']
                lat=latlon[0]
                lon=latlon[1]
                properties=i['properties']
                geomtype=i['geometry']['type']
                for k,v in properties.items():
                    j="""%s=%s""" % (k,v)
                    formatted_properties+=j
                detaillist.append(formatted_properties)
                pointsitems.append(0)
                pointsitems.append(lat)
                pointsitems.append(lon)
                pointsitems.append(c)
            pointslist.append(pointsitems)
            c+=1
            maplat=pointslist[0][1]
            maplon=pointslist[0][2]
    else:
        jsonstr = json.dumps(d, indent=4)	
        return HttpResponse(jsonstr, status=d['status'],
                                mimetype='application/json')
        
    
    return render_to_response("multimarkers.html", {'pointslist': pointslist,
                                                    'detaillist': detaillist,
                                                    'maplat': maplat,
                                                    'maplon': maplon,
                                                    },
                              context_instance = RequestContext(request),)

def render_points_client_side(request, kwargs):
    """
        Do the same as render_points, but client side.
    """
    pass_to_browser = {
        'data_url': "/api/1.0/features/search?%s" % urllib.urlencode(kwargs),
        'query_attributes': kwargs
    }
    return render_to_response("cs_multimarkers.html", {'map_data': json.dumps(pass_to_browser), 'widepage': True})
    
def render_features_in_country_subdivision(request, country_subdivision_code):
    """ Return geographic feature matching subdivision_code. """
    country_subdivision_code = country_subdivision_code.upper()
    split_values=country_subdivision_code.split("-")
    if len(split_values)==1:
        kwargs={'country_code':split_values[0]}
    if len(split_values)==2:
        kwargs={'country_code':split_values[0],'subdivision_code': split_values[1]}
    return render_points(request, kwargs)
    
def render_search_features(request):
    kwargs= dict(request.GET.items())
    if kwargs.has_key('country_code'):
        kwargs['country_code']=kwargs['country_code'].upper() 
    if kwargs.has_key('subdivision_code'):
        kwargs['subdivision_code']=kwargs['subdivision_code'].upper()
    return render_points(request, kwargs)