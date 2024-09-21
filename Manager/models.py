from django.db import models
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
