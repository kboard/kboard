from urllib.parse import urlencode
from django import template

register = template.Library()


@register.simple_tag
def url_parameter(**kwargs):
    return '?'+urlencode(kwargs)
