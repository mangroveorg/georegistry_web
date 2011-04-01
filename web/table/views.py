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
from georegistry_web.web.gmap.utils import query_georegistry
import urllib

    
def table_points(request, kwargs):
    """
        Plot multiple points based on a kwarg dict
    """
    data = urllib.urlencode(kwargs) 
    URL="api/1.0/features/search?%s" % (data)
    r= query_georegistry(URL)
    d=json.loads(r)
    if d['status']==200:
        total=d['total']
        gr_id_list=[]
        column_names= d.keys()
        
        for i in d['features']:
            c=0
            pointsitems=[]
            column_names.append(i.keys())
            column_names.append(i['geometry'].keys())
            print column_names
            geomtype=i['geometry']['type']
            if geomtype=="Point": 
                gr_id=i['properties']['id']
                gr_name=i['properties']['name']
                
                gr_id_list.append({'gr_id': gr_id, 'gr_name': gr_name })
    else:
        jsonstr = json.dumps(d, indent=4)	
        return HttpResponse(jsonstr, status=d['status'],
                                mimetype='application/json')
        
    return render_to_response("list.html", {'gr_id_list': gr_id_list,
                                            'total': total },
                              context_instance = RequestContext(request),)
    
    
def table_search_features(request):
    kwargs= dict(request.GET.items())
    if kwargs.has_key('country_code'):
        kwargs['country_code']=kwargs['country_code'].upper() 
    if kwargs.has_key('subdivision_code'):
        kwargs['subdivision_code']=kwargs['subdivision_code'].upper()
    return table_points(request, kwargs)