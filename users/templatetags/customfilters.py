from django import template

register = template.Library()

def count(obj):
    return len(obj)

register.filter('count', count)
