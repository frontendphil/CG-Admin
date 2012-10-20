from django.conf.urls import patterns, url

urlpatterns = patterns("admin.views.docs", 
    url(r'^$', 'search', name='search_docs'),
    url(r'^page/(?P<page>\d+)/$', 'list', name='list_docs_page'),
    url(r'^query/(?P<query>(\w+|\s)+)/page/(?P<page>\d+)/$', 'list', name='list_docs'),
    url(r'^(?P<id>\d+)/$','show', name='show_doc'),
    url(r'^delete/(?P<id>\d+)/$', 'delete', name='delete_doc'),
    url(r'^edit/(?P<id>\d+)/$', 'edit', name='edit_doc'),
)