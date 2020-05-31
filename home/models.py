from django.db import models


class Demande(models.Model):
    value = models.CharField(max_length=500)
    validators = models.CharField(max_length=500)
    valide = models. BooleanField(default=False)