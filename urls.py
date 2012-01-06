from django.conf.urls.defaults import *
from trials_site.views import *
# from haystack import search
#Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from sitemap import *

sitemaps = {'trial':TrialSitemap}

urlpatterns = patterns('',
    (r'^$', home),
    (r'^notify/', email),
    (r'^search/$', search),
    (r'^trial/', trial),
#    (r'haystack', haystack.search),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^unsubscribe/([A=Za-z0-9]*@[A-Za-z0-9]*\.[a-z]*)/$', unsubscribe),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)    
