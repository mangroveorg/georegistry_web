#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'^renderpoint/(?P<feature_id>[^/]+)/$', render_point,
                                                 name="render_point"),
    
    #get all features for a country or subdivision (i.e. state) (returns a google map)
    url(r'^location/(?P<country_subdivision_code>[^/]+)/$',
        render_features_in_country_subdivision,
        name="render_features_in_country_subdivision"),
    
    url(r'^search/$',render_search_features, name="render_search_features")

)