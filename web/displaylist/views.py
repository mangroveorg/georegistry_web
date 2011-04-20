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

    
def displaylist_points(request, kwargs):
    """
        Plot multiple points based on a kwarg dict
    """
    data = urllib.urlencode(kwargs) 
    URL="api/1.0/features/search?%s" % (data)
    r= query_georegistry(URL)
    d=json.loads(r)
    if d['status']==200:

        return render_to_response("web/display.html", {'d': r},
                              context_instance = RequestContext(request),)
        
    else:
        jsonstr = json.dumps(d, indent=4)	
        return HttpResponse(jsonstr, status=d['status'],
                                mimetype='application/json')
        

    
def displaylist_features_in_country_subdivision(request, country_subdivision_code):
    """ Return geographic feature matching subdivision_code. """
    country_subdivision_code = country_subdivision_code.upper()
    split_values=country_subdivision_code.split("-")
    if len(split_values)==1:
        kwargs={'country_code':split_values[0]}
    if len(split_values)==2:
        kwargs={'country_code':split_values[0],'subdivision_code': split_values[1]}
    return displaylist_points(request, kwargs)
    
def displaylist_search_features(request):
    kwargs= dict(request.GET.items())
    if kwargs.has_key('country_code'):
        kwargs['country_code']=kwargs['country_code'].upper() 
    if kwargs.has_key('subdivision_code'):
        kwargs['subdivision_code']=kwargs['subdivision_code'].upper()
    return displaylist_points(request, kwargs)