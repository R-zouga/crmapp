from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.apps import AppConfig
from django.utils import timezone


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "User"


@receiver(user_logged_out)
def sig_user_logged_out(sender, user, **kwargs):
    """A Receiver that always stores last logout time of User instance."""
    user.last_logout = timezone.now()
    user.save()
