from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    phone_number = models.CharField(max_length=12, unique=True)

    class Status(models.TextChoices):
        salesman = "Salesman", _("Salesman")
        branch_supervisor = "Branch Supervisor", _("Branch Supervisor")
        department_manager = "Department Manager", _("Department Manager")
        client = "Client", _("Client")
        representative = "Representative", _("Representative")

    current_status = models.CharField(max_length=40, choices=Status)


class UserHistory(models.Model):
    branch = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now=True)
    quit_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=40)


class Salesman(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branches = models.ManyToManyField("BranchGroup")
    max_enrolled_branches = models.PositiveSmallIntegerField(default=1)


class BranchSupervisor(models.Model):
    branch_group = models.OneToOneField("BranchGroup", on_delete=models.CASCADE)
    departments = models.ManyToManyField("DepartmentBoard")


class DepartmentManager(models.Model):
    department = models.OneToOneField("DepartmentBoard", on_delete=models.CASCADE)
    managers_group = models.ManyToManyField("ManagerGroup")


class Client(models.Model):
    employees = models.ManyToManyField("Salesman", through="Deal")


class Deal(models.Model):
    class Status(models.IntegerChoices):
        interested = 0
        first_meeting = 1
        further_motivation = 2
        acquired = 100
        lost = -1

    salesman = models.ForeignKey(Salesman, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_of_state = models.DateField(auto_now=True)
    status = models.IntegerField(choices=Status, default=Status.interested)


class Representative(models.Model):
    companies = models.ManyToManyField("Company")


class Company(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    location = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.name


class CategoryGroup(models.Model):
    group = models.ManyToManyField(Group)

    def __str__(self):
        return self.group.name

    class Meta:
        abstract = True


class BranchGroup(CategoryGroup):
    max_members = models.PositiveSmallIntegerField(default=5)


class DepartmentBoard(CategoryGroup):
    pass


class ManagerGroup(CategoryGroup):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
