# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='starts_with')
def starts_with(value, arg):
    """
    Returns True if the value (string) starts with the given arg (string).
    """
    if isinstance(value, str) and isinstance(arg, str):
        return value.startswith(arg)
    return False
