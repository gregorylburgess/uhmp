from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'uhmp.views.status', name='status'),
    url(r'^update/(?P<objType>.+)/(?P<ID>.+)/(?P<status>.+)/(?P<currentZone>.+)?$', 'uhmp.views.update'),
    url(r'^status/', 'uhmp.views.status', name='status'),
    url(r'^graph/', 'uhmp.views.graph', name='graph'),
    url(r'^getgraph/(?P<place>.+)/(?P<time>.+)$', 'uhmp.views.getgraph'),
    url(r'^list/(?P<currentZone>.+)$', 'uhmp.views.lelist'),
    url(r'^list/', 'uhmp.views.lelist', name='lelist'),
    url(r'^admin/', include(admin.site.urls)),
)
