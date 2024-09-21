from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

