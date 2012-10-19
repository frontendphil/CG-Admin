from datetime import date


from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from admin.models import User, Patient, Prescription
from admin.decorators import require_login, anonymous_only

@require_login
def index(request):
    now = date.today()
    patients = Patient.objects.filter(birthday__day=now.day, birthday__month=now.month)

    return render_to_response("index.html", 
                              locals(), 
                              context_instance=RequestContext(request))


@require_login
def verify(request, patient, prescription=0):
    try:
        patient = Patient.objects.get(pk=patient)
    except Patient.DoesNotExist:
        return redirect("add_patient")
    
    try:
        prescription = Prescription.objects.get(pk=prescription)
    except Prescription.DoesNotExist:
        prescription = None

    return render_to_response("verify.html",
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

@require_login
def logout(request):
    request.session.pop("user")

    return redirect("login")