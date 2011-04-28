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
    
def browse(request, country_code):
    """
        Plot multiple points based on a kwarg dict
    """
    #data = urllib.urlencode(kwargs) 
    if country_code:
        URL="api/1.0/features/locations?country_code=%s" % (country_code)
    else:
        URL="api/1.0/features/locations"
    r = query_georegistry(URL)
    
    locations = json.loads(r)
    #print type(locations)
    
    country_name=locations.keys()[0]
    locations=locations[country_name]['children']
    return render_to_response("web/browse.html", {'country_name': country_name.title(),
                                                  'country_code': country_code,
                                                  'locations': locations},
                              context_instance = RequestContext(request),)


def browsecountries(request):
    """
        Plot multiple points based on a kwarg dict
    """
    #data = urllib.urlencode(kwargs) 

    URL="api/1.0/features/countries"
    l = query_georegistry(URL)
    countries = json.loads(l)
    return render_to_response("web/countries.html", {'countries': countries},
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