from django import template

register = template.Library()


@register.simple_tag
def url_parameter(**kwargs):
    if len(kwargs):
        url_string = '?'
        cnt = 0
        for key in kwargs:
            if cnt != 0:
                url_string += '&'
            url_string += str(key) + '=' + str(kwargs[key])
            cnt += 1

        return url_string
    else:
        return ''
