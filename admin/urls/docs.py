from django.conf.urls import patterns, url

urlpatterns = patterns("admin.views.docs", 
    url(r'^(?P<id>\d+)/$','show', name='show_doc'),
    url(r'^(?P<id>\d+)/delete$','delete', name='delete_doc'),
    url(r'^(?P<id>\d+)/edit$','edit', name='edit_doc'),
)