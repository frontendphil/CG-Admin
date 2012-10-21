from django.conf.urls import patterns, url, include

urlpatterns = patterns('admin.views.patient', 
    url(r'^(?P<id>\d+)/$', 'show', name='show_patient'),
    url(r'^(?P<id>\d+)/delete/$', 'delete', name='delete_patient'),
    url(r'^(?P<id>\d+)/delete/redirect/(?P<after>\w+)/$', 'delete', name='delete_patient_redirect'),
    url(r'^(?P<id>\d+)/edit/$', 'edit', name='edit_patient'),
    url(r'^(?P<id>\d+)/save/$', 'save', name='save_patient'),
    url(r'^(?P<id>\d+)/save/prescription/(?P<pid>\d+)/$', 'save', name='save_all'),
    url(r'^(?P<id>\d+)/continue/$', 'finish', name='continue_patient'),

    url(r'^(?P<id>\d+)/prescription/(?P<pid>\d+)/template/$', 'show', name='prescription_template'),
    url(r'^(?P<id>\d+)/prescription/', include("admin.urls.prescription")),

    url(r'^add/$', 'add', name='add_patient'),
    url(r'^add/next/$', 'add', { "cont": True }, name="add_patient_next_step"),
)