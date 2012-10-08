from datetime import date, timedelta

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.db.models import Q

from cgadmin import settings

from forms import PatientForm, PrescriptionForm
from models import Patient, Doctor, Prescription, User
from decorators import login_required, anonymous_only
from templatetags.admin_extras import get_query

@login_required
def index(request):
    DEBUG = settings.DEBUG

    now = date.today()
    patients = Patient.objects.filter(birthday__day=now.day, birthday__month=now.month)

    return render_to_response("index.html", 
                              locals(), 
                              context_instance=RequestContext(request))

@login_required
def add_patient(request):
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

    return render_to_response("add_patient.html",
                               locals(),
                               context_instance=RequestContext(request))    

@login_required
def continue_patient(request):
    if "continue" in request.GET:
        patient = Patient.objects.get(dirty=True)

        if request.GET.get("continue") == "1":
            request.session["patient_id"] = patient.id

            return redirect("add_prescription")
        else:
            request.session.pop("patient_id")

            patient.delete()

            return redirect("add_patient")

    return render_to_response("continue_patient.html",
                              locals(),
                              context_instance=RequestContext(request))

@login_required
def add_prescription(request):
    try:
        patient = Patient.objects.get(pk=request.session.get("patient_id"))
    except Patient.DoesNotExist:
        return redirect("add_patient")

    if request.method == "POST":
        form = PrescriptionForm(request.POST)

        if form.is_valid():
            prescription = Prescription.from_form(form, patient)

            prescription.save()

            request.session["prescription_id"] = prescription.id

            return redirect('verify')
    else:
        try: 
            prescription = Prescription.objects.get(dirty=True)
        except Prescription.DoesNotExist:
            prescription = None

        if prescription:
            return redirect("verify")

        form = PrescriptionForm()

    return render_to_response("add_prescription.html",
                              locals(),
                              context_instance=RequestContext(request))

@login_required
def verify(request):
    try:
        patient = Patient.objects.get(pk=request.session.get("patient_id"))
    except Patient.DoesNotExist:
        return redirect("add_patient")
    
    try:
        prescription = Prescription.objects.get(pk=request.session.get("prescription_id"))
    except Prescription.DoesNotExist:
        prescription = None

    return render_to_response("verify.html",
                              locals(),
                              context_instance=RequestContext(request))

@require_POST
@login_required
def save_patient(request):
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

@login_required
def edit_patient(request):
    pass

@login_required
@require_POST
def delete_patient(request):
    pass

@login_required
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

    return render_to_response("search.html", 
                              locals(),
                              context_instance=RequestContext(request))

@login_required
def docs(request):
    query = request.GET.get("query")

    if query:
        q = get_query(query, ["name", "key", "address__street", "address__city"])

        docs_list = Doctor.objects.filter(q)
    else:
        docs_list = Doctor.objects.all()

    paginator = Paginator(docs_list, 25)

    page = request.GET.get("page")

    try:
        docs = paginator.page(page)
    except PageNotAnInteger:
        docs = paginator.page(1)
    except EmptyPage:
        docs = paginator.page(paginator.num_pages)

    return render_to_response("docs.html",
                              locals(),
                              context_instance=RequestContext(request))

@login_required
def docs_delete(request, id):
    pass

@login_required
def docs_edit(request, id):
    return render_to_response("doc_edit.html",
                              locals(),
                              context_instance=RequestContext(request))

@anonymous_only
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.login(username, password)

        if user:
            request.session["user"] = user.id

            return redirect("index")

    return render_to_response("login.html",
                              locals(),
                              context_instance=RequestContext(request))

@login_required
def logout(request):
    request.session.pop("user")

    return redirect("login")