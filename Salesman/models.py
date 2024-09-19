from django.db import models
from django.utils import timezone


class Salesman(models.Model):
    user = models.OneToOneField(
        "User", on_delete=models.CASCADE, primary_key=True, db_column="user_email"
    )
    branches = models.ManyToManyField("BranchGroup", related_name="salesmen_set")
    max_enrolled_branches = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name_plural = "Salesmen"


class Deal(models.Model):
    """Deal class is the most important model that stores ALL SERVICES provided
    to the clients and companies' representatives."""

    class Status(models.IntegerChoices):
        interested = 0
        first_meeting = 1
        further_motivation = 2
        acquired = 100
        lost = -1

    salesman = models.ForeignKey(
        Salesman, on_delete=models.CASCADE, db_column="salesman_email"
    )
    attributed_to = models.ForeignKey(
        "BranchGroup", on_delete=models.CASCADE, db_column="branch_name"
    )
    service_seeker = models.ForeignKey(
        "User", on_delete=models.CASCADE, db_column="seeker_email"
    )
    representing = models.ForeignKey(
        "Company", on_delete=models.CASCADE, db_column="company_name", null=True
    )
    service = models.ForeignKey(
        "Service", on_delete=models.CASCADE, db_column="service_name"
    )
    date_of_state = models.DateTimeField(default=timezone.now)
    status = models.SmallIntegerField(choices=Status, default=Status.interested)

    class Meta:
        ordering = ["-date_of_state"]
