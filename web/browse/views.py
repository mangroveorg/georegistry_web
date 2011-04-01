# Create your views here.
try:
    import json
except ImportError:
    import simplejson as json

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from georegistry_web.web.gmap.utils import query_georegistry
import urllib
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import *
    
def browse(request, kwargs):
    """
        Plot multiple points based on a kwarg dict
    """
    data = urllib.urlencode(kwargs) 
    URL="api/v1/features/search?%s" % (data)
    
    r= query_georegistry(URL)
    d=json.loads(r)
    if d['status']==200:
        total=d['total']
        gr_id_list=[]
    
        for i in d['features']:
            c=0
            pointsitems=[]
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
    
def by_country_and_subdivision(request):
    
    
    if request.method == 'POST':
        kwargs= dict(request.POST.items())
        kwargs['country_subdivision_code'] = kwargs['country_subdivision_code'].upper()
        split_values=kwargs['country_subdivision_code'].split("-")
        if len(split_values)==1:
            kwargs={'country_code':split_values[0]}
        if len(split_values)==2:
            kwargs={'country_code':split_values[0],'subdivision_code': split_values[1]}
        print kwargs
        return browse(request, kwargs)

    
    return render_to_response('web/browse/by_country_and_subdivision.html', 
                             {'form': FeatureUploadForm()},
                              context_instance = RequestContext(request))
    
    
    
    
    kwargs= dict(request.GET.items())
    if kwargs.has_key('country_code'):
        kwargs['country_code']=kwargs['country_code'].upper() 
    if kwargs.has_key('subdivision_code'):
        kwargs['subdivision_code']=kwargs['subdivision_code'].upper()
    return browse(request, kwargs)