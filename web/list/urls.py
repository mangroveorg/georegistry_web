#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    
    #get all features for a country or subdivision (i.e. state) (returns a google map)
    url(r'^location/(?P<country_subdivision_code>[^/]+)/$',
        list_features_in_country_subdivision,
        name="list_features_in_country_subdivision"),
    
    url(r'^search/$', list_search_features, name="list_search_features")

)