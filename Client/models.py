from django.db import models


class Client(models.Model):
    user = models.OneToOneField(
        "User", on_delete=models.CASCADE, primary_key=True, db_column="user_email"
    )
