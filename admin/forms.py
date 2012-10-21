# -*- coding: utf-8 -*-

from django import forms
from django.forms.util import ErrorList

from models import Patient, Prescription, Doctor

def xor(a, b):
    return (not not a) != (not not b)

class CGForm(forms.Form):
    def get(self, field):
        return self[field]

class PatientForm(CGForm):
    gender = forms.ChoiceField(widget=forms.Select, choices=Patient.GENDERS)
    
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'span4'}))
    surname = forms.CharField(widget=forms.TextInput(attrs={'class':'span4'}))

    day = forms.IntegerField(widget=forms.TextInput(attrs={
        'class':'input-mini',
        'placeholder':'Tag'
    }))

    month = forms.IntegerField(widget=forms.TextInput(attrs={
        'class':'input-mini',
        'placeholder': 'Monat'
    })) 

    year = forms.IntegerField(widget=forms.TextInput(attrs={
        'class':'input-mini',
        'placeholder':'Jahr'
    }))

    street = forms.CharField(widget=forms.TextInput(attrs={
        'class':'span3',
        'placeholder':'Straße'
    }))

    nr = forms.CharField(max_length=5, widget=forms.TextInput(attrs={
        'class':'span1',
        'placeholder':'Nr'
    }))

    code = forms.IntegerField(widget=forms.TextInput(attrs={
        'class':'span1',
        'placeholder':'PLZ'
    }))

    city = forms.CharField(widget=forms.TextInput(attrs={
        'class':'span3',
        'placeholder':'Stadt'
    }))

    phone_private_code = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'span2',
        'placeholder': 'Vorwahl'
    }))

    phone_private_nr = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'span2',
        'placeholder': 'Rufnummer'
    }))

    phone_office_code = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'span2',
        'placeholder': 'Vorwahl'
    }))

    phone_office_nr = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'span2',
        'placeholder': 'Rufnummer'
    }))

    state = forms.ChoiceField(widget=forms.RadioSelect, choices=Patient.STATES)

    insurance_name = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class': 'span1',
        'placeholder': 'Name'
    }))

    insurance_nr = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'span3',
        'placeholder': 'Versicherungsnummer'
    }))

    @classmethod
    def from_patient(cls, patient):
        return cls(patient.get_form_data())

    def is_valid(self):
        valid = True

        if not super(PatientForm, self).is_valid():
            valid = False

        if not self["state"].value() == Patient.STATE_PRIVATE[0]:
            if self["insurance_name"].value() == "":
                self._errors["insurance_name"] = ErrorList(u"Kassenname fehtl")

            if self["insurance_nr"].value() == "":
                self._errors["insurance_nr"] = ErrorList(u"Versicherungsnummer fehlt")

            valie = valid and not (self["insurance_name"].value() == "" or self["insurance_nr"].value() == "")

        if xor(self["phone_private_code"].value(), self["phone_private_nr"].value()):
            self._errors["phone_private_code"] = ErrorList(u"Nummer unvollständig")

            valid = False

        if xor(self["phone_office_code"].value(), self["phone_office_nr"].value()):
            self._errors["phone_office_code"] = ErrorList(u"Nummer unvollständig")

            valid = False

        return valid

class PrescriptionForm(CGForm):
    day = forms.IntegerField(widget=forms.TextInput(attrs={
        'class':'input-mini',
        'placeholder': 'Tag'
    }))

    month = forms.IntegerField(widget=forms.TextInput(attrs={
        'class':'input-mini',
        'placeholder':'Monat'
    }))

    year = forms.IntegerField(widget=forms.TextInput(attrs={
        'class':'input-mini',
        'placeholder': 'Jahr'
    }))

    diagnosis = forms.CharField(widget=forms.Textarea(attrs={
        'class':'span4',
        'rows':5
    }))

    cure = forms.CharField(widget=forms.TextInput(attrs={
        'class':'span4'
    }))

    kind = forms.ChoiceField(widget=forms.RadioSelect, choices=Prescription.KINDS)

    visit = forms.BooleanField(required=False, initial=False)

    report = forms.BooleanField(required=False, initial=False)

    amount = forms.IntegerField(widget=forms.TextInput(attrs={
        'class':'span4'
    }))

    count = forms.CharField(widget=forms.TextInput(attrs={
        'class':'span4'
    }))

    indicator = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'span4'
    }))

    doctor = forms.ModelChoiceField(required=False, queryset=Doctor.objects.all(), widget=forms.Select(attrs={
        'class':'span4'
    }))

    appointments = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class':'span4',
        'rows':5
    }))

    new_doc = forms.BooleanField(required=False, widget=forms.HiddenInput(attrs={
        'class': 'add_new_doc',
        'value': '0'
    }))

    @classmethod
    def from_prescription(cls, prescription):
        return cls(prescription.get_form_data())

    def is_valid(self):
        valid = super(PrescriptionForm, self).is_valid()

        if self["new_doc"].value() == "0":
            if not self["doctor"].value():
                return False

        return valid