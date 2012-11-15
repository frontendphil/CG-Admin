from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.http import require_POST

from admin.models import Prescription, Patient
from admin.forms import PrescriptionForm, DoctorForm
from admin.decorators import require_login


@require_login
def add(request, id, pid=None):
    try:
        patient = Patient.objects.get(pk=id)
    except Patient.DoesNotExist:
        return redirect("add_patient")

    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        doc = DoctorForm(request.POST)

        if form.is_valid() and (form.get("new_doc").value() == "0" or doc.is_valid()):
            prescription = Prescription.from_form(form, patient=patient, doctor=doc)
            prescription.save()

            if patient.dirty:
                return redirect('verify', patient=patient.id, prescription=prescription.id)
            else:
                prescription.dirty = False
                prescription.save()

                return redirect("show_patient", id=patient.id)
        else:
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
            return redirect("verify", patient=patient.id, prescription=prescription.id)

        form = PrescriptionForm()

    return render_to_response("prescription/add.html",
                              locals(),
                              context_instance=RequestContext(request))


@require_login
@require_POST
def delete(request, id, pid):
    prescription = get_object_or_404(Prescription, pk=pid)
    prescription.delete()

    return redirect("show_patient", id=id)


@require_login
def edit(request, id, pid):
    prescription = get_object_or_404(Prescription, pk=pid)
    patient = get_object_or_404(Patient, pk=id)

    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        doc = DoctorForm(request.POST)

        if form.is_valid() and (form.get("new_doc") == "0" or doc.is_valid()):
            prescription = Prescription.from_form(form, patient=patient, prescription=prescription)

            prescription.save()

            return redirect("show_patient", id=id)
    else:
        form = PrescriptionForm.from_prescription(prescription, True)
        doc = DoctorForm()

    return render_to_response("prescription/edit.html",
                              locals(),
                              context_instance=RequestContext(request))
