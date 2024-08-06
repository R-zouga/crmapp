from django.db import models

from user.models import Deal


class Service(models.Model):
    deal = models.OneToOneField(Deal, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.PositiveIntegerField()
