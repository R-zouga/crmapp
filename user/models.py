from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


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


class User(AbstractUser):
    email = models.EmailField(primary_key=True)
    phone_number = models.CharField(max_length=12, unique=True)
    last_logout = models.DateTimeField(null=True, blank=True)
    current_status = models.CharField(max_length=40)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def username(self):
        return self.get_username()


class UserHistory(models.Model):
    class Status(models.TextChoices):
        salesman = "Salesman", _("Salesman")
        branch_supervisor = "Supervisor", _("Supervisor")
        department_manager = "Manager", _("Manager")
        client = "Client", _("Client")
        representative = "Representative", _("Representative")

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_email")
    join_date = models.DateTimeField(default=timezone.now)
    quit_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=40, choices=Status)
    responsible_for = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, db_column="responsible_for_name")
    belonging_to = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="belonging_set", db_column="belonging_to_name")


class Salesman(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    branches = models.ManyToManyField("BranchGroup")
    max_enrolled_branches = models.PositiveSmallIntegerField(default=1)


class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    branch_group = models.OneToOneField("BranchGroup", on_delete=models.CASCADE)
    departments = models.ManyToManyField("DepartmentBoard")


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    department = models.OneToOneField("DepartmentBoard", on_delete=models.CASCADE)
    managers_group = models.ManyToManyField("ManagerGroup")


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    salesmen = models.ManyToManyField("Salesman", through="Deal")


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
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    companies = models.ManyToManyField("Company")


class Company(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    email = models.EmailField()
    location = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.name


class CategoryGroup(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    groups = models.ManyToManyField(Group)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class BranchGroup(CategoryGroup):
    max_members = models.PositiveSmallIntegerField(default=5)


class DepartmentBoard(CategoryGroup):
    pass


class ManagerGroup(CategoryGroup):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
