from django.db import models

class Patient(models.Model):
	GENDERS = (
		("Male", "m"),
		("Female", "f")
	)

	STATES = (
		("Private", "p"),
		("Public", "k")
	)

	name = models.CharField(max_length=255)
	surname = models.CharField(max_length=255)

	birthday = models.DateField()

	gender = models.CharField(choices=GENDERS, max_length=1)

	phone = models.CharField(max_length=20)

	state = models.CharField(choices=STATES, max_length=1)

	address = models.ForeignKey("Address")
	insurance = models.ManyToManyField("Insurance", through="Insured")

	def __unicode__(self):
		return "%s, %s" % (self.surname, self.name)

class Insured(models.Model):
	patient = models.ForeignKey("Patient")
	insurance = models.ForeignKey("Insurance")

	nr = models.CharField(max_length=255)

class Address(models.Model):
	street = models.CharField(max_length=255)
	nr = models.CharField(max_length=5)

	city_code = models.IntegerField()

	city = models.CharField(max_length=255)

class Insurance(models.Model):
	name = models.CharField(max_length=255)