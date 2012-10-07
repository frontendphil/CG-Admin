from django.template import Library

register = Library()

@register.filter
def get_range(value):
    return range(value)

@register.filter
def get_natural_range(value):
    return [i + 1 for i in range(value)]