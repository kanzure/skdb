from django.conf.urls.defaults import *

# Databrowse registration:

from django.contrib.auth.decorators import login_required
from django.contrib import databrowse
from fjarlog.models import Budget
import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# admin.autodiscover()
# databrowse.site.register(Budget)

urlpatterns = patterns('',
    # Example:
    # (r'^sources/', include('sources.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^admin/(.*)', admin.site.root),
    (r'^databrowse/(.*)', login_required(databrowse.site.root)),

    (r'^$', 'basesite.views.index'),

    (r'^dmed/$', 'fabmap.views.index'),
    (r'^dmed/getsite', 'fabmap.views.getsite'),
    (r'^dmed/addsite', 'fabmap.views.addsite'),
    (r'^dmed/search', 'fabmap.views.search'),
    (r'^dmed/sitedetails', 'fabmap.views.sitedetails'),
    (r'^xml/site', 'fabmap.views.sitetoxml'),
    (r'^yaml/site', 'fabmap.views.sitetoyaml'),
    (r'^xmlrpc/$', 'xmlrpc.views.handle_xmlrpc'),
)



if settings.DEBUG:
        urlpatterns += patterns('', (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/smari/www/tangiblebit.com/media'}),)
