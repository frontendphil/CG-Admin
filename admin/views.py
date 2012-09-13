from django.shortcuts import render_to_response
from django.template import RequestContext

from cgadmin import settings

def index(request):
    DEBUG = settings.DEBUG

    return render_to_response("index.html", 
                              locals(), 
                              context_instance=RequestContext(request))

def add_patient(request):
    return render_to_response("add_patient.html",
                               locals(),
                               context_instance=RequestContext(request))    

def add_prescription(request):
    return render_to_response("add_prescription.html",
                              locals(),
                              context_instance=RequestContext(request))