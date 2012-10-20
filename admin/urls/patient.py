from django.conf.urls import patterns, url

urlpatterns = patterns('admin.views.patient', 
    url(r'^find/$', "search", name="search_patient"),
    url(r'^(?P<id>\d+)/$', 'show', name='show_patient'),
    url(r'^(?P<id>\d+)/prescription/(?P<prescription>\d+)/$', 'show', name='prescription_template'),
    url(r'^add/$', 'add', name='add_patient'),
    url(r'^continue/$', 'finish', name='continue_patient'),
    url(r'^save/$', 'save', name='save_all'),
    url(r'^edit/(?P<id>\d+)/$', 'edit', name='edit_patient'),
    url(r'^delete/(?P<id>\d+)/$', 'delete', name='delete_patient'),   
)