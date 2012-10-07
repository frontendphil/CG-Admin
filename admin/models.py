# -*- coding: utf-8 -*-
import json
from hashlib import sha256

from httplib import HTTPConnection

from django.db import models

from time import strptime, strftime

def get(form, field, default = None):
    return form.get(field).value() or default

def get_date_string(form):
    return "%s.%s.%s" % (get(form, "day"),
                         get(form, "month"),
                         get(form, "year"))

def get_phone_number(form, kind):
    if get(form, "phone_%s_code" % kind) or get(form, "phone_%s_nr" % kind):
        return "%s/%s" % (get(form, "phone_%s_code" % kind), get(form, "phone_%s_nr" % kind))

    return ""

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

class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    @classmethod
    def register(cls, username, password):
        try:
            user = cls.objects.get(username=username)
        except cls.DoesNotExist:
            user = cls.objects.create(username=username, password=sha256(password).hexdigest())

        return user

    @classmethod
    def login(cls, username, password):
        try:
            user = cls.objects.get(username=username, password = sha256(password).hexdigest())
        except cls.DoesNotExist:
            user = None

        return user

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
    def load(cls, filename):
        f = file(filename)

        data = json.loads(f.read())

        for patient in data:
            

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

    def is_incomplete(self):
        return not self.street or not self.nr or not self.city_code or not self.city

    def __unicode__(self):
        if self.street or self.nr:
            return u"%s %s in %s %s" % (self.street, self.nr, self.city_code, self.city)

        return u"%s %s" % (self.city_code, self.city)

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

    @classmethod
    def from_form(cls, form, patient=None):
        if not patient or not form.is_valid():
            return None

        prescription = cls()
        prescription.date = strftime("%Y-%m-%d", strptime(get_date_string(form), "%d.%m.%Y"))
        prescription.diagnosis = get(form, "diagnosis")
        prescription.cure = get(form, "cure")
        prescription.kind = get(form, "kind")
        prescription.visit = get(form, "visit", False)
        prescription.report = get(form, "report", False)
        prescription.amount = get(form, "amount")
        prescription.count = get(form, "count")
        prescription.indicator = get(form, "indicator")

        if get(form, "new_doc") == "1":
            doctor = Doctor.from_form(form)
        else:
            doctor = Doctor.objects.get(pk=get(form, "doctor"))

        prescription.doctor = doctor
        prescription.appointments = get(form, "appointments", "")

        prescription.patient = patient

        return prescription

    date = models.DateField()

    diagnosis = models.TextField()
    cure = models.CharField(max_length=255)

    kind = models.CharField(max_length=1, choices=KINDS)

    visit = models.BooleanField(default=False)
    report = models.BooleanField(default=False)

    amount = models.IntegerField()
    count = models.CharField(max_length=10)

    indicator = models.CharField(max_length=10)

    doctor = models.ForeignKey("Doctor")

    appointments = models.TextField()

    patient = models.ForeignKey(Patient)

    dirty = models.BooleanField(default=True)

    def get_kind(self):
        for key, value in self.KINDS:
            if key == self.kind:
                return value

class Doctor(models.Model):
    name = models.CharField(max_length=255)

    address = models.ForeignKey(Address)
    phone = models.CharField(max_length=40)
    key = models.CharField(max_length=50)

    dirty = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    @classmethod
    def from_form(cls, form):
        pass

    @classmethod
    def parse_street(cls, data):
        if not data:
            return None

        data = data.replace(".", ". ")

        parts = data.split(" ")

        if len(parts) == 1:
            return (parts[0], "")

        street = " ".join(parts[0:-1])
        nr = parts[::-1][0]

        try:
            int(nr)
        except ValueError:
            if "." in nr:
                clean_nr = nr.split(".")

                street += ".".join(clean_nr[0:-1])
                nr = clean_nr[::-1][0]

        return (street, nr)

    @classmethod
    def load(cls, filename):
        f = file(filename)

        data = json.loads(f.read())

        for doc in data:
            if not doc["name"]:
                continue

            result = cls()
            result.name = doc["name"]
            result.phone = doc["phone"]
            result.key = doc["key"]

            street = cls.parse_street(doc["address"]["street"])
            address = None

            if street:
                try:
                    address = Address.objects.get(street=street[0], 
                                                  nr=street[1],
                                                  city_code=int(doc["address"]["code"]))
                except Address.DoesNotExist:
                    pass

            if not address:
                address = Address()

                if street:
                    address.street = street[0]
                    address.nr = street[1]

                address.city_code = int(doc["address"]["code"])

                city = doc["address"]["city"]

                if not city:
                    connection = HTTPConnection("maps.google.com")
                    connection.request("GET", "http://maps.google.com/maps/geo?q=%d,Deutschland&output=json" % int(doc["address"]["code"]))

                    response = connection.getresponse()
                    res_json = json.loads(response.read())
                    
                    try:
                        address.city = res_json["Placemark"][0]["AddressDetails"]["Country"]["AdministrativeArea"]["Locality"]["LocalityName"]
                    except KeyError:
                        pass
                else:
                    address.city = doc["address"]["city"]

                address.save()

            result.address = address
            result.dirty = False

            result.save()

    def is_incomplete(self):
        return not self.name or not self.key or len(self.phone) < 2 or self.address.is_incomplete()

    def __unicode__(self):
        return u"%s" % self.name