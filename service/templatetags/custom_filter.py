import datetime
from django import template
from django.utils.timezone import localtime

register = template.Library()


@register.filter
def custom_date(value):
    today = datetime.date.today()
    time_str = localtime(value).strftime("%H:%M")  # Format time as 'HH:MM'

    if value.date() == today:
        return f"Today at {time_str}"
    elif value.date() == today + datetime.timedelta(days=1):
        return f"Tomorrow at {time_str}"
    elif value.date() == today - datetime.timedelta(days=1):
        return f"Yesterday at {time_str}"
    else:
        return value.strftime("%A, %d/%m/%Y at %H:%M")
