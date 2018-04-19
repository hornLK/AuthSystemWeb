from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()

@register.filter
def get_key(dic,key):
    return json.loads(dic).get(key)
