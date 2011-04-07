from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:

    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

    #(r'^display/', direct_to_template, {'template': 'web/display.html'}),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^', include('georegistry_web.web.urls')),



)
