import re

from django import template

register = template.Library()


@register.simple_tag
def hide_ip(ip):
    m = re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', str(ip))
    if m is not None:
        ip_arr = str(ip).split('.')
        ip_arr[2] = 'xxx'
        return '.'.join(ip_arr)
    else:
        return str(ip)