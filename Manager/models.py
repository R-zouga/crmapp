from django.db import models

from Client.models import Client
from User.models import User, CategoryGroup
from Supervisor.models import DepartmentBoard


class Manager(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, db_column="user_email"
    )
    department = models.OneToOneField(
        DepartmentBoard, on_delete=models.CASCADE, db_column="department_name"
    )
    managers_group = models.ManyToManyField("ManagerGroup")


class ManagerGroup(CategoryGroup):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, db_column="admin_email")


class AskUpgrade(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, db_column="client_email", primary_key=True)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, db_column="manager_email")