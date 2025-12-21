from django import template

register = template.Library()


@register.filter
def sum_field(items, field_name):
    """Sum a field across items"""
    total = 0
    for item in items:
        value = getattr(item, field_name, 0)
        if value:
            total += float(value)
    return total

