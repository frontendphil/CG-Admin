from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from cgadmin import settings
from forms import PatientForm

def index(request):
    DEBUG = settings.DEBUG

    return render_to_response("index.html", 
                              locals(), 
                              context_instance=RequestContext(request))

def add_patient(request):
    if request.method == "POST":
        form = PatientForm(request.POST)

        if form.is_valid():
            if "next" in request.GET:
                return redirect(request.GET["next"])

            return redirect('index')
    else:
        form = PatientForm()

    return render_to_response("add_patient.html",
                               locals(),
                               context_instance=RequestContext(request))    

def add_prescription(request):
    return render_to_response("add_prescription.html",
                              locals(),
                              context_instance=RequestContext(request))