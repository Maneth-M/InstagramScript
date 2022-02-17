from django.template import Library
import datetime

register = Library()

@register.filter(expects_localtime=True)
def parse_iso(value):
    value = str(value)
    return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")