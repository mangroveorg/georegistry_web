#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.conf.urls.defaults import *
from views import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^countries$', browsecountries, name="browsecountries"),
    url(r'^(?P<country_code>[^/]+)$', browse, name="browse"),
    #url(r'^by-country/$', by_country, name="by_country"),
    #url(r'^by-country-and-subdivision/$', by_country_and_subdivision, name="by_country_and_subdivision")

)