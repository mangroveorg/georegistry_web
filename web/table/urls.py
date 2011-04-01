#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    
    url(r'^search/$', table_search_features, name="table_search_features")

)