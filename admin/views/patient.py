from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.http import require_POST

from admin.decorators import require_login
from admin.models import Patient
from admin.forms import PatientForm, PrescriptionForm
from admin.templatetags.admin_extras import get_query

@require_login
def add(request):
    if request.method == "POST":
        form = PatientForm(request.POST)

        if form.is_valid():
            patient = Patient.from_form(form)

            if "next" in request.GET:
                request.session["patient_id"] = patient.id

                return redirect(request.GET["next"])

            patient.dirty = False
            patient.save()

            return redirect('index')
    else:
        try:
            patient = Patient.objects.get(dirty = True)
        except Patient.DoesNotExist:
            patient = None

        if patient:
            return redirect("continue_patient")

        form = PatientForm()

    return render_to_response("patient/add.html",
                               locals(),
                               context_instance=RequestContext(request))  

@require_login
def finish(request):
    if "continue" in request.GET:
        patient = Patient.objects.get(dirty=True)

        if request.GET.get("continue") == "1":
            request.session["patient_id"] = patient.id

            return redirect("add_prescription")
        else:
            request.session.pop("patient_id")

            patient.delete()

            return redirect("add_patient")

    return render_to_response("patient/continue.html",
                              locals(),
                              context_instance=RequestContext(request))

@require_POST
@require_login
def save(request):
    patient = Patient.objects.get(pk=request.session.get("patient_id"))
    patient.dirty = False
    patient.save()

    request.session.pop("patient_id")

    try:
        prescription = Prescription.objects.get(pk=request.session.get("prescription_id"))
    except Prescription.DoesNotExist:
        prescription = None

    if prescription:
        prescription.dirty = False
        prescription.save()

        request.session.pop("prescription_id")

    return redirect("index")

@require_login
def show(request, id):
    patient = get_object_or_404(Patient, pk=id)

    if patient.state == "k":
        insurance = patient.insured_set.all()[0]

    # prescriptions = patient.prescription_set.all().order_by("-date")

    form = PrescriptionForm()

    return render_to_response("patient/view.html",
                              locals(),
                              context_instance=RequestContext(request))

@require_login
def edit(request):
    pass

@require_login
@require_POST
def delete(request, id):
    patient = get_object_or_404(Patient, pk=id)
    patient.delete()

    return redirect("search_patient")

@require_login
def search(request):
    query = request.GET.get("query")

    if query:
        q = get_query(query, ["name", "surname", "address__street", "address__city", "birthday"])

        patients_list = Patient.objects.filter(q)
        paginator = Paginator(patients_list, 25)

        page = request.GET.get("page")

        try:
            patients = paginator.page(page)
        except PageNotAnInteger:
            patients = paginator.page(1)
        except EmptyPage:
            patients = paginator.page(paginator.num_pages)

    return render_to_response("patient/search.html", 
                              locals(),
                              context_instance=RequestContext(request))