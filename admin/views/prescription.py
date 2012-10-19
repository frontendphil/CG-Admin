from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.http import require_POST

from admin.models import Prescription, Patient
from admin.forms import PrescriptionForm
from admin.decorators import require_login

@require_login
def add(request, patient):
    try:
        patient = Patient.objects.get(pk=patient)
    except Patient.DoesNotExist:
        return redirect("add_patient")

    if request.method == "POST":
        form = PrescriptionForm(request.POST)

        if form.is_valid():
            prescription = Prescription.from_form(form, patient)

            prescription.save()

            request.session["prescription_id"] = prescription.id

            if patient.dirty:
                return redirect('verify')

        # set new prescription active
        
        if not patient.dirty:
            return render_to_response("patient/view.html",
                                      locals(),
                                      context_instance=RequestContext(request))

    else:
        try: 
            prescription = Prescription.objects.get(dirty=True)
        except Prescription.DoesNotExist:
            prescription = None

        if prescription:
            return redirect("verify")

        form = PrescriptionForm()

    return render_to_response("prescription/add.html",
                              locals(),
                              context_instance=RequestContext(request))

@require_login
@require_POST
def delete(request, patient, prescription):
    prescription = get_object_or_404(Prescription, pk=prescription)
    prescription.delete()

    return redirect("show_patient", id=patient)