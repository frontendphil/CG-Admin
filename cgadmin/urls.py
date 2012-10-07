from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('admin.views',
	url(r'^$', 'index', name='index'),
	url(r'^add/patient/$', 'add_patient', name='add_patient'),
	url(r'^add/prescription/$', 'add_prescription', name='add_prescription'),
    url(r'^verify/patient/$', 'verify', name='verify'),
    url(r'^continue/patient/$', 'continue_patient', name='continue_patient'),
    url(r'^save/patient/$', 'save_patient', name='save_all'),

    url(r'^search/$', 'search', name='search'),

    url(r'^docs/$', 'docs', name='docs'),
    url(r'^docs/delete/(?P<id>\d+)/$', 'docs_delete', name='delete_doc'),
    url(r'^docs/edit/(?P<id>\d+)/$', 'docs_edit', name='edit_doc'),

    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
