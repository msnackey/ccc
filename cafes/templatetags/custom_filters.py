from datetime import datetime, timezone

from django import template

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
def custom_timesince(value):  # TODO: Localize
    """Custom timesince filter to return minutes, hours or days since datetime."""
    if not value:
        return ""

    now = datetime.now(timezone.utc)
    timedelta = now - value

    if timedelta.total_seconds() < 60:
        return "just now"

    elif timedelta.total_seconds() < 3600:
        minutes, seconds = divmod(timedelta.total_seconds(), 60)
        if minutes == 1:
            return "1 minute ago"
        return f"{minutes:.0f} minutes ago"

    elif timedelta.days < 1:
        hours, remainder = divmod(timedelta.total_seconds(), 3600)
        return f"{hours:.0f} hours ago"

    elif timedelta.days < 31:
        if timedelta.days == 1:
            return "1 day ago"
        return f"{timedelta.days} days ago"

    elif timedelta.days < 366:
        months = timedelta.days * 12 / 365.25
        if int(months) == 1:
            return "1 month ago"
        return f"{months:.0f} months ago"

    else:
        years = timedelta.days / 365.25
        if int(years) == 1:
            return "1 year ago"
        return f"{years:.0f} years ago"
