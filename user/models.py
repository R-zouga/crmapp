from django.contrib.auth.models import User, Group
from django.db import models


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.user.username

    class Meta:
        abstract = True


class CategoryGroup(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.group.name

    class Meta:
        abstract = True


class Employee(Person):
    branches = models.ManyToManyField("BranchGroup", through="WorkPeriod")
    max_enrolled_branches = models.PositiveSmallIntegerField(default=1)


class WorkPeriod(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    branch_group = models.ForeignKey("BranchGroup", on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now_add=True)
    date_left = models.DateField(blank=True, null=True)


class BranchSupervisor(Person):
    branch_group = models.OneToOneField("BranchGroup", on_delete=models.CASCADE)


class DepartmentManager(Person):
    department = models.OneToOneField("DepartmentBoard", on_delete=models.CASCADE)


class Client(Person):
    employees = models.ManyToManyField("Employee", through="Deal")


class Deal(models.Model):
    class Status(models.IntegerChoices):
        interested = 0
        first_meeting = 1
        further_motivation = 2
        acquired = 100
        lost = -1

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_of_state = models.DateField(auto_now_add=True)
    status = models.IntegerField(choices=Status, default=Status.interested)


class Represedddddntative(Person):
    companies = models.ManyToManyField("Company")


class BranchGroup(CategoryGroup):
    max_members = models.PositiveIntegerField(default=5)

    # def add_member(self, user):
    #     if self.group.user_set.count() < self.max_members:
    #         self.group.user_set.add(user)
    #     else:
    #         raise ValueError("Cannot add more members to this group.")


class DepartmentBoard(models.Model):
    department_manager = models.ForeignKey(DepartmentManager, on_delete=models.CASCADE)


class Company(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    location = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.name
