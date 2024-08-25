from datetime import date

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import (
    BaseUserManager,
    PermissionsMixin,
    Permission,
    GroupManager,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from service.models import Service


class Group(models.Model):
    name = models.CharField(_("name"), max_length=150, primary_key=True)
    permissions = models.ManyToManyField(Permission, verbose_name=_("permissions"), related_name="custom_group_set")

    objects = GroupManager()
    
    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=12, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_logout = models.DateTimeField(null=True, blank=True)
    current_status = models.CharField(max_length=40)
    groups = models.ManyToManyField(Group)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        unique_together = ["first_name", "last_name"]


class UserHistory(models.Model):
    class Status(models.TextChoices):
        salesman = "Salesman", _("Salesman")
        branch_supervisor = "Supervisor", _("Supervisor")
        department_manager = "Manager", _("Manager")
        client = "Client", _("Client")
        representative = "Representative", _("Representative")

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_email")
    join_date = models.DateField(default=date.today)
    quit_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=40, choices=Status)
    responsible_for = models.ForeignKey(
        Group, on_delete=models.CASCADE, null=True, db_column="responsible_for_name"
    )
    belonging_to = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="belonging_set",
        db_column="belonging_to_name",
    )

    class Meta:
        ordering = ["-join_date"]


class Salesman(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, db_column="user_email"
    )
    branches = models.ManyToManyField("BranchGroup")
    max_enrolled_branches = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name_plural = _("Salesmen")


class Supervisor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, db_column="user_email"
    )
    branch_group = models.OneToOneField(
        "BranchGroup", on_delete=models.CASCADE, db_column="branch_name"
    )
    departments = models.ManyToManyField("DepartmentBoard")


class Manager(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, db_column="user_email"
    )
    department = models.OneToOneField(
        "DepartmentBoard", on_delete=models.CASCADE, db_column="department_name"
    )
    managers_group = models.ManyToManyField("ManagerGroup")


class Client(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, db_column="user_email"
    )


class Deal(models.Model):
    class Status(models.IntegerChoices):
        interested = 0
        first_meeting = 1
        further_motivation = 2
        acquired = 100
        lost = -1

    salesman = models.ForeignKey(
        Salesman, on_delete=models.CASCADE, db_column="salesman_email"
    )
    service_seeker = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column="client_email"
    )
    attributed_to = models.ForeignKey("BranchGroup", on_delete=models.CASCADE, db_column="branch_name")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, db_column="service_name")
    date_of_state = models.DateField(auto_now_add=True)
    status = models.SmallIntegerField(choices=Status, default=Status.interested)

    class Meta:
        ordering = ["-date_of_state"]


class Representative(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, db_column="user_email"
    )
    companies = models.ManyToManyField("Company")


class Company(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    email = models.EmailField()
    location = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.name


class CategoryGroup(models.Model):
    group = models.OneToOneField(
        Group, on_delete=models.CASCADE, db_column="group_name", primary_key=True
    )

    def __str__(self):
        return self.group.name

    class Meta:
        abstract = True


class BranchGroup(CategoryGroup):
    max_members = models.PositiveSmallIntegerField(default=30)


class DepartmentBoard(CategoryGroup):
    pass


class ManagerGroup(CategoryGroup):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, db_column="admin_email")
