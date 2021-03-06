from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()




urlpatterns = patterns('',
    #Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^search/$', 'cms.search.views.search'),
    (r'^weblog/categories/', include('coltrane.urls.categories')),
    (r'^weblog/links/', include('coltrane.urls.links')),
    (r'^weblog/tags/', include('coltrane.urls.tags')),
    (r'^weblog/', include('coltrane.urls.entries')),
    (r'', include('django.contrib.flatpages.urls')),


    
    #(r'^tiny_mce/(?:<path>.*)$', 'django.views.static.serve', {'document root': '/tinymce/jscripts/tiny_mce/' }),

)

