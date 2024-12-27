from datetime import datetime, timezone

from django import template
from django.utils.timesince import timesince

register = template.Library()


@register.filter
def star(value: float) -> str:
    """Returns a five letter string to signify how many stars should be rendered based on the given float"""
    rounded_value = round(value * 2) / 2

    if rounded_value.is_integer():
        return ("f" * int(rounded_value)) + ("e" * (5 - int(rounded_value)))
    else:
        return ("f" * int(rounded_value)) + "h" + ("e" * (4 - int(rounded_value)))


@register.filter
def custom_timesince(value):
    """Custom timesince filter to exclude hours/minutes if time exceeds one day."""
    if not value:
        return ""

    now = datetime.now(timezone.utc)
    delta = now - value

    time_str = timesince(value, now)

    if delta.days >= 1:
        return time_str.split(",")[0]

    return time_str
