import json

from django import template

register = template.Library()

@register.filter()
def to_int_json(value):
    return int(json.loads(value))

