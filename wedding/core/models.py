from django.db import models


class Rsvp(models.Model):
    family_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    notes = models.CharField(max_length=200)


class Guest(models.Model):
    rsvp = models.ForeignKey(Rsvp, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    meal = models.CharField(max_length=64)
    safari = models.CharField(max_length=32)