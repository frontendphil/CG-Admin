from django.conf.urls import patterns, include, url

urlpatterns = patterns('admin.views.app',
    url(r'^$', 'index', name='index'),

    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),

    url(r'^patient/', include("admin.urls.patient")),
    url(r'^doc/', include("admin.urls.docs")),

    url(r'^search/', include("admin.urls.search")),

    url(r'^verify/patient/(?P<patient>\d+)/prescription/(?P<prescription>\d*)$', 'verify', name='verify'),
    url(r'^verify/patient/(?P<patient>\d+)/$', 'verify', name='verify_only_patient'),
)
