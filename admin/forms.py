from django import forms

from models import Patient

class PatientForm(forms.Form):
    gender = forms.ChoiceField(widget=forms.Select, choices=Patient.GENDERS)
    
    name = forms.CharField()
    surname = forms.CharField()

    day = forms.IntegerField()
    month = forms.IntegerField()
    year = forms.IntegerField()

    street = forms.CharField()
    nr = forms.CharField(max_length=5)

    code = forms.IntegerField()
    city = forms.CharField()

    phone_private_code = forms.CharField(required=False)
    phone_private_nr = forms.CharField(required=False)

    phone_office_code = forms.CharField(required=False)
    phone_office_nr = forms.CharField(required=False)

    state = forms.ChoiceField(widget=forms.RadioSelect, choices=Patient.STATES)

    insurance_name = forms.CharField(required=False)
    insurance_nr = forms.CharField(required=False)

class PrescriptionForm(forms.Form):
    pass