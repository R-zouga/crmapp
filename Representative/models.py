from django.db import models
from User.models import User


class Representative(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, db_column="user_email"
    )
    companies = models.ManyToManyField("Company", related_name="companies_set")


class Company(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    email = models.EmailField()
    location = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.name
