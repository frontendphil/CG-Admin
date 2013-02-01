from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.http import HttpResponse

from admin.decorators import require_login
from admin.models import Patient, Prescription
from admin.forms import PatientForm, PrescriptionForm, DoctorForm
from admin.templatetags.admin_extras import get_query
from admin.utils import PDFWriter


@require_login
def add(request, cont=False):
    if request.method == "POST":
        form = PatientForm(request.POST)

        if form.is_valid():
            patient = Patient.from_form(form)

            if cont:
                return redirect("add_prescription", id=patient.id)

            patient.dirty = False
            patient.save()

            return redirect('index')
    else:
        try:
            patient = Patient.objects.get(dirty=True)
        except Patient.DoesNotExist:
            patient = None

        if patient:
            return redirect("continue_patient", id=patient.id)

        form = PatientForm()

    return render_to_response("patient/add.html",
                               locals(),
                               context_instance=RequestContext(request))


@require_login
def finish(request, id):
    patient = Patient.objects.get(pk=id)

    url_attachment = reverse("index")

    return render_to_response("patient/continue.html",
                              {
                                "patient": patient,
                                "url_attachment": url_attachment
                              },
                              context_instance=RequestContext(request))


@require_POST
@require_login
def save(request, id, pid=None):
    patient = Patient.objects.get(pk=id)
    patient.dirty = False
    patient.save()

    if pid:
        prescription = Prescription.objects.get(pk=pid)
        prescription.dirty = False
        prescription.save()

    return redirect("index")


@require_login
def pdf(request, id):
    patient = get_object_or_404(Patient, pk=id)

    writer = PDFWriter()

    return HttpResponse(writer.pdf_for_patient(patient), mimetype="application/pdf")


@require_login
def show(request, id, pid=None, complete=False):
    patient = get_object_or_404(Patient, pk=id)

    if patient.state == "k":
        insurance = patient.get_insurance()

    if pid:
        prescription = Prescription.objects.get(pk=pid)

        form = PrescriptionForm.from_prescription(prescription)
    else:
        form = PrescriptionForm()

    doc = DoctorForm()

    return render_to_response("patient/view.html",
                              locals(),
                              context_instance=RequestContext(request))

@require_login
def show_doc(request, id, pid):
    patient = get_object_or_404(Patient, pk=id)
    prescription = get_object_or_404(Prescription, pk=pid)
    doctor = prescription.doctor

    return render_to_response("docs/view.html",
                              locals(),
                              context_instance=RequestContext(request))


@require_login
def edit(request, id):
    patient = get_object_or_404(Patient, pk=id)

    if request.method == "POST":
        form = PatientForm(request.POST)

        if form.is_valid():
            patient = Patient.from_form(form, patient=patient)
            patient.save()

            return redirect("%s#%s" % (reverse("show_patient", args=(id,)), request.GET.get("forward", "")))
    else:
        form = PatientForm.from_patient(patient)

    url_attachment = request.GET.get("forward", None)

    return render_to_response("patient/edit.html",
                              locals(),
                              context_instance=RequestContext(request))


@require_login
@require_POST
def delete(request, id):
    patient = get_object_or_404(Patient, pk=id)
    patient.delete()

    return redirect(request.GET.get("forward", reverse("search_patient")))


@require_login
def list(request, query=None, page=1):
    if query and query == "None":
        return redirect("list_patients_page", page=page)

    if query:
        q = get_query(query, ["name", "surname", "address__street", "address__city", "birthday"])

        patients_list = Patient.objects.filter(q)
        paginator = Paginator(patients_list, 25)

        try:
            patients = paginator.page(page)
        except PageNotAnInteger:
            patients = paginator.page(1)
        except EmptyPage:
            patients = paginator.page(paginator.num_pages)

    return render_to_response("patient/search.html",
                              locals(),
                              context_instance=RequestContext(request))


@require_login
def search(request):
    query = request.GET.get("query")

    if query:
        return redirect("list_patients", query=query, page=1)

    return redirect("list_patients_page", page=1)
