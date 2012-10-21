from django.conf.urls import patterns, url

urlpatterns = patterns("admin.views.prescription",
    url(r'^add/$', 'add', name='add_prescription'),

    url(r'^(?P<pid>\d+)/add/$', 'add', name='add_prescription_template'),
    url(r'^(?P<pid>\d+)/delete/$', 'delete', name='delete_prescription'),
    url(r'^(?P<pid>\d+)/edit/$', 'edit', name='edit_prescription'),
)