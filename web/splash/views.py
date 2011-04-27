# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from utils import fetch_countries_count, fetch_categories_count, fetch_total_count
from utils import fetch_country_count

def splash(request):
 #countries=fetch_countries_count()
 MGCount=fetch_country_count('MG')
 
 NGCount=fetch_country_count('NG')

 categories=fetch_categories_count()
 total= fetch_total_count()
 return render_to_response("web/splash.html", {'MGCount': MGCount, 'NGCount': NGCount,
                                              'categories': categories,
                                               'total': total,
                                               },
                              context_instance = RequestContext(request),)
    