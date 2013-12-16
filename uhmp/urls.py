from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'uhmp.views.status', name='status'),
    url(r'^status/', 'uhmp.views.status', name='status'),
    url(r'^graph/', 'uhmp.views.graph', name='graph'),
    url(r'^list/(?P<currentZone>.+)/$', 'uhmp.views.lelist'),
    url(r'^list/', 'uhmp.views.lelist', name='lelist'),
    url(r'^admin/', include(admin.site.urls)),
)
