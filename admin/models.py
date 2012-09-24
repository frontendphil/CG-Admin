# -*- coding: utf-8 -*-
from django.db import models

from time import strptime, strftime

def get(form, field):
    return form.get(field).value()

def get_date_string(form):
    return "%s.%s.%s" % (get(form, "day"),
                         get(form, "month"),
                         get(form, "year"))

def get_phone_number(form, kind):
    return "%s/%s" % (get(form, "phone_%s_code" % kind), get(form, "phone_%s_nr" % kind))

def get_address(form):
    street = get(form, "street")
    nr = get(form, "nr")
    code = get(form, "code")

    try:
        address = Address.objects.get(street=street, nr=nr, city_code=code)
    except Address.DoesNotExist:
        address = Address()
        address.street = street
        address.nr = nr
        address.city_code = code
        address.city = get(form, "city")
        address.save()

    return address

def get_insurance(form, patient):
    try:
        insurance = Insurance.objects.get(name=get(form, "insurance_name"))
    except Insurance.DoesNotExist:
        insurance = Insurance()
        insurance.name = get(form, "insurance_name")
        insurance.save()

    insured = Insured()
    insured.patient = patient
    insured.insurance = insurance
    insured.nr = get(form, "insurance_nr")

    insured.save()

    return insured

class Patient(models.Model):
    GENDERS = (
        ("m", "Herr"),
        ("f", "Frau")
    )

    STATE_PRIVATE = ("p", "Privatpatient")

    STATES = (
        STATE_PRIVATE,
        ("k", "Kassenpatient")
    )

    dirty = models.BooleanField(default=True)

    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)

    birthday = models.DateField()

    gender = models.CharField(choices=GENDERS, max_length=1)

    phone_private = models.CharField(max_length=20)
    phone_office = models.CharField(max_length=20)

    state = models.CharField(choices=STATES, max_length=1)

    address = models.ForeignKey("Address")
    insurance = models.ManyToManyField("Insurance", through="Insured")

    @classmethod
    def from_form(cls, form):
        if not form.is_valid():
            return None

        patient = Patient()
        patient.name = get(form, "name")
        patient.surname = get(form, "surname")
        patient.gender = get(form, "gender")

        patient.birthday = strftime("%Y-%m-%d", strptime(get_date_string(form), "%d.%m.%Y"))

        patient.phone_private = get_phone_number(form, "private")
        patient.phone_office = get_phone_number(form, "office")

        patient.state = get(form, "state")

        patient.address = get_address(form)

        if not patient.state == cls.STATE_PRIVATE:
            patient.save()

            get_insurance(form, patient)

        patient.save()

        return patient

    def __unicode__(self):
        return u"%s, %s" % (self.surname, self.name)

class Insured(models.Model):
    patient = models.ForeignKey("Patient")
    insurance = models.ForeignKey("Insurance")

    nr = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s - %s (%s)" % (self.patient, self.insurance, self.nr)

class Address(models.Model):
    street = models.CharField(max_length=255)
    nr = models.CharField(max_length=5)

    city_code = models.IntegerField()

    city = models.CharField(max_length=255)

    def __unicode__(self):
        return u"%s %s in %s %s" % (self.street, self.nr, self.city_code, self.city)

class Insurance(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u"%s" % self.name

class Prescription(models.Model):
    KINDS = (
        ("e", "Erstverordnung"),
        ("f", "Folgeverordnung"),
        ("v", "Verordnung außerhalb des Regelfalls"),
    )

    date = models.DateField()

    diagnosis = models.TextField()
    cure = models.CharField(max_length=255)

    kind = models.CharField(max_length=1, choices=KINDS)

    visit = models.BooleanField(default=False)
    report = models.BooleanField(default=False)

    amount = models.IntegerField()
    count = models.IntegerField()

    indicator = models.CharField(max_length=10)

    doctor = models.ForeignKey("Doctor")

    appointments = models.TextField()

    patient = models.ForeignKey(Patient)

class Doctor(models.Model):
    name = models.CharField(max_length=255)

    address = models.ForeignKey(Address)

    def __unicode__(self):
        return u"%s" % self.name