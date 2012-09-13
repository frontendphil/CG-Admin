from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('admin.views',
	url(r'^$', 'index', name='index'),
	url(r'^add/patient/$', 'add_patient', name='add_patient'),
	url(r'^add/prescription/$', 'add_prescription', name='add_prescription'),
    # Examples:
    # url(r'^$', 'cgadmin.views.home', name='home'),
    # url(r'^cgadmin/', include('cgadmin.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
