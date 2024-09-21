from datetime import date

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import (
    BaseUserManager,
    PermissionsMixin,
    Permission,
    GroupManager,
)
from django.db import models


class Group(models.Model):
    """
    Creating a custom Group model which is the same copy of Group Class in admin app.

    The reason for this is to alter the primary key to be the name of the group instead of an id field.
    """

    name = models.CharField("name", max_length=150, primary_key=True)
    permissions = models.ManyToManyField(
        Permission, verbose_name="permissions", related_name="custom_group_set"
    )

    objects = GroupManager()

    def __str__(self):
        """Return the name of the group."""
        return self.name


class CustomUserManager(BaseUserManager):
    """Subclassing BaseUserManager to override user model methods for creating User instances."""

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
    """
    User model of the project.

    A couple of fields are added and some default ones are removed.
    """

    email = models.EmailField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # added fields
    phone_number = models.CharField(max_length=12, unique=True)
    last_logout = models.DateTimeField(null=True, blank=True)
    current_status = models.CharField(max_length=40)

    # making sure that the ManyToMany Relationship is with the custom Group Class
    groups = models.ManyToManyField(Group)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        """Return the email of the user."""
        return self.email

    @property
    def full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}"

    class Meta:
        # making sure that full_name of user is unique in the database.
        unique_together = ["first_name", "last_name"]


class UserHistory(models.Model):
    """
    A model that keeps track of history of User instance within the company.
    """

    class Status(models.TextChoices):
        salesman = "Salesman", "Salesman"
        branch_supervisor = "Supervisor", "Supervisor"
        department_manager = "Manager", "Manager"
        client = "Client", "Client"
        representative = "Representative", "Representative"

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_email")
    join_date = models.DateField(default=date.today)
    quit_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=40, choices=Status)
    responsible_for = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=True,
        related_name="responsible_for_set",
        db_column="responsible_for_name",
    )
    belonging_to = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="belonging_to_set",
        null=True,
        db_column="belonging_to_name",
    )

    class Meta:
        ordering = ["-join_date"]


class CategoryGroup(models.Model):
    """An abstract base class that all categories (BranchGroup, DepartmentBoard, ManagerGroup) inherit from."""

    group = models.OneToOneField(
        Group, on_delete=models.CASCADE, db_column="group_name", primary_key=True
    )

    def __str__(self):
        return self.group.name

    class Meta:
        abstract = True
