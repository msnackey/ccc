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
