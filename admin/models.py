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
        return Address.objects.get(street__iexact=street, nr=nr, city_code=code)
    except Address.DoesNotExist:
        return Address.objects.create(street=street,
                                      nr=nr,
                                      city_code=code,
                                      city=get(form, "city"))

def create_insurance(patient, insurance_name, insurance_nr):
    if not insurance_name:
        insurance = Insurance.get_blank_insurance()
    else:
        try:
            insurance = Insurance.objects.get(name__iexact=insurance_name)
        except Insurance.DoesNotExist:
            insurance = Insurance.objects.create(name=insurance_name)

    return Insured.objects.create(patient=patient,
                                  insurance=insurance,
                                  nr=insurance_nr)

def get_insurance_from_form(form, patient):
    return create_insurance(patient, get(form, "insurance_name"), get(form, "insurance_nr"))

def parse_street(data):
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

def get_or_create_address(data):
    street = parse_street(data["address"]["street"])
    address = None

    if street:
        try:
            address = Address.objects.get(street=street[0], 
                                          nr=street[1],
                                          city_code=int(data["address"]["code"]))
        except Address.DoesNotExist:
            pass

    if not address:
        address = Address()

        if street:
            address.street = street[0]
            address.nr = street[1]

        address.city_code = int(data["address"]["code"])

        city = data["address"]["city"]

        if not city:
            connection = HTTPConnection("maps.google.com")
            connection.request("GET", "http://maps.google.com/maps/geo?q=%d,Deutschland&output=json" % int(data["address"]["code"]))

            response = connection.getresponse()
            res_json = json.loads(response.read())
            
            try:
                address.city = res_json["Placemark"][0]["AddressDetails"]["Country"]["AdministrativeArea"]["Locality"]["LocalityName"]
            except KeyError:
                pass
        else:
            address.city = data["address"]["city"]

        address.save()

    return address

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

    birthday = models.DateField(null=True)

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
            result = cls()

            result.name = patient["name"]
            result.surname = patient["surname"]

            if not "null" in patient["birthday"]:
                result.birthday = strftime("%Y-%m-%d", strptime(patient["birthday"], "%d.%m.%Y"))

            result.phone_private = patient["phone_private"]
            result.phone_office = patient["phone_office"]

            result.state = "p" if patient["private"] else "k"
            result.gender = patient["gender"]
            result.address = get_or_create_address(patient)

            result.dirty = False

            result.save()

            if not patient["private"]:
                create_insurance(result, patient["insurance"]["name"], patient["insurance"]["nr"])

            for prescription in patient["prescriptions"]:
                Prescription.load(prescription, result)

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

            get_insurance_from_form(form, patient)

        patient.save()

        return patient

    def get_birthday(self):
        return self.birthday.strftime("%d.%m.%Y") if self.birthday else ""

    def __unicode__(self):
        return u"%s, %s" % (self.surname, self.name)

class Insured(models.Model):
    patient = models.ForeignKey("Patient")
    insurance = models.ForeignKey("Insurance")

    nr = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s (%s)" % (self.insurance, self.nr)

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
    is_blank = models.BooleanField(default=False)

    @classmethod
    def get_blank_insurance(cls):
        try:
            return cls.objects.get(is_blank=True)
        except cls.DoesNotExist:
            return Insurance.objects.create(is_blank=True, name="")

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

    date = models.DateField(null=True)

    diagnosis = models.TextField()
    cure = models.CharField(max_length=255)

    kind = models.CharField(max_length=1, choices=KINDS)

    visit = models.BooleanField(default=False)
    report = models.BooleanField(default=False)

    amount = models.CharField(max_length=10)
    count = models.CharField(max_length=10)

    indicator = models.CharField(max_length=10)

    doctor = models.ForeignKey("Doctor", null=True)

    appointments = models.TextField()

    patient = models.ForeignKey(Patient)

    dirty = models.BooleanField(default=True)

    @classmethod
    def load(cls, json, patient):
        p = cls()
        p.diagnosis = json["diagnosis"]
        p.cure = json["treatment"]
        
        if json["prescription"] == "1":
            p.kind = "e"
        elif json["prescription"] == "2":
            p.kind = "f"
        elif json["prescription"] == "3":
            p.kind = "v"
        else:
            p.kind = ""

        p.visit = json["visit"]
        p.report = json["report"]
        p.indicator = json["key"]
        p.amount = json["amount"] or 0
        p.count = json["count"] or 0

        if json["doctor"]:
            p.doctor = Doctor.objects.get(name__iexact=json["doctor"]["name"])
        else:
            p.doctor = None

        p.appointments = json["appointments"]
        
        try:
            p.date = strftime("%Y-%m-%d", strptime(json["date"], "%d.%m.%Y"))
        except ValueError:
            p.date = None

        p.dirty = False
        p.patient = patient

        p.save()

    def get_date(self):
        return self.date.strftime("%d.%m.%Y")

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

            result.address = get_or_create_address(doc)
            result.dirty = False

            result.save()

    def is_incomplete(self):
        return not self.name or not self.key or len(self.phone) < 2 or self.address.is_incomplete()

    def __unicode__(self):
        return u"%s" % self.name