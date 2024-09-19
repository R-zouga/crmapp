from django.db import models


class Supervisor(models.Model):
    user = models.OneToOneField(
        "User", on_delete=models.CASCADE, primary_key=True, db_column="user_email"
    )
    branch_group = models.OneToOneField(
        "BranchGroup", on_delete=models.CASCADE, db_column="branch_name"
    )
    departments = models.ManyToManyField("DepartmentBoard")
