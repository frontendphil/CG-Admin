from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.http import HttpResponse

from admin.models import Prescription, Patient
from admin.forms import PrescriptionForm, DoctorForm
from admin.decorators import require_login
from admin.utils import PDFWriter


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

                return redirect("%s#%s" % (reverse("show_patient", args=(patient.id,)), request.GET.get("forward", "")))
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
def pdf(request, id, pid, official=False):
    prescription = get_object_or_404(Prescription, pk=pid)
    patient = get_object_or_404(Patient, pk=id)

    writer = PDFWriter()
    pdf = writer.pdf_for_prescription(patient, prescription, official)

    return HttpResponse(pdf, mimetype="application/pdf")


@require_login
@require_POST
def delete(request, id, pid):
    prescription = get_object_or_404(Prescription, pk=pid)
    prescription.delete()

    return redirect("%s#%s" % (reverse("show_patient", args=(id,)), request.GET.get("forward", "")))


@require_login
def edit(request, id, pid):
    prescription = get_object_or_404(Prescription, pk=pid)
    patient = get_object_or_404(Patient, pk=id)

    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        doc = DoctorForm(request.POST)

        if form.is_valid() and (form.get("new_doc").value() == "0" or doc.is_valid()):
            prescription = Prescription.from_form(form, patient=patient, prescription=prescription, doctor=doc)

            prescription.save()

            return redirect("%s#%s" % (reverse("show_patient", args=(id,)), request.GET.get("forward", "")))
    else:
        form = PrescriptionForm.from_prescription(prescription, True)
        doc = DoctorForm()

    url_attachment = request.GET.get("forward", None)

    return render_to_response("prescription/edit.html",
                              locals(),
                              context_instance=RequestContext(request))
