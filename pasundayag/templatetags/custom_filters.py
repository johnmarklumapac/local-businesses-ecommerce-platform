from django import template

app_name = 'pasundayag'

register = template.Library()

def attr(field, args):
    """
    Adds HTML attributes to a form field.
    Usage: {{ form.field_name|attr:"attr1:value1 attr2:value2" }}
    """
    attrs = {}
    for arg in args.split():
        try:
            name, value = arg.split(':')
            attrs[name] = value
        except ValueError:
            pass
    return field.as_widget(attrs=attrs)

register.filter('attr', attr)