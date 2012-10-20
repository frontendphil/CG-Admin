from django.conf.urls import patterns, url

urlpatterns = patterns("admin.views.prescription",
    url(r'^add/patient/(?P<patient>\d+)/$', 'add', name='add_prescription'),
    url(r'^add/patient/(?P<patient>\d+)/template/(?P<template>\d+)/$', 'add', name='add_prescription_template'),
    url(r'^delete/patient/(?P<patient>\d+)/prescription/(?P<prescription>\d+)/$', "delete", name="delete_prescription"),
)