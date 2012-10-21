from django.conf.urls import patterns, url

urlpatterns = patterns("admin.views", 
    url(r'^patient/$', "patient.search", name="search_patient"),
    url(r'^patient/page/(?P<page>\d+)/$', 'patient.list', name='list_patients_page'),
    url(r'^patient/query/(?P<query>(\w+|\s)+)/page/(?P<page>\d+)/$', 'patient.list', name='list_patients'),

    url(r'^doc/$', "docs.search", name="search_docs"),
    url(r'^doc/page/(?P<page>\d+)/$', 'docs.list', name='list_docs_page'),
    url(r'^doc/query/(?P<query>(\w+|\s)+)/page/(?P<page>\d+)/$', 'docs.list', name='list_docs'),
)