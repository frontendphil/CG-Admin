from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from cgadmin import settings

from forms import PatientForm, PrescriptionForm
from models import Patient

def index(request):
    DEBUG = settings.DEBUG

    return render_to_response("index.html", 
                              locals(), 
                              context_instance=RequestContext(request))

def add_patient(request):
    if request.method == "POST":
        form = PatientForm(request.POST)

        if form.is_valid():
            patient = Patient.from_form(form)

            if "next" in request.GET:
                return redirect(request.GET["next"])

            patient.dirty = False
            patient.save()

            return redirect('index')
    else:
        form = PatientForm()

    return render_to_response("add_patient.html",
                               locals(),
                               context_instance=RequestContext(request))    

def add_prescription(request):
    if request.method == "POST":
        form = PrescriptionForm(request.POST)

        if form.is_valid():
          return redirect('verify_patient')
    else:
        form = PrescriptionForm()

    return render_to_response("add_prescription.html",
                              locals(),
                              context_instance=RequestContext(request))

def verify_patient(request):
    pass