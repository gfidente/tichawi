from django import template
register = template.Library()

@register.filter
def votes_to_human(value):
    return int(value) / 10 - 10
