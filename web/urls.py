#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    #add url paths for our web apps here
    #url(r'^/', direct_to_template, {'template': 'web/index.html'}),
    (r'webhook/', include('georegistry_web.web.webhook.urls')),
    (r'gmap/', include('georegistry_web.web.gmap.urls')),
    (r'list/', include('georegistry_web.web.list.urls')),
    (r'display/', include('georegistry_web.web.displaylist.urls')),
    (r'table/', include('georegistry_web.web.table.urls')),
    (r'browse/', include('georegistry_web.web.browse.urls')),
    url(r'^$', direct_to_template, {'template': 'web/splash.html'}),
)