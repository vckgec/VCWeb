from django import template
from mess.forms import StoreKeeperForm
register = template.Library()

@register.assignment_tag
def set(val=-1):
    val+=1
    return val

@register.assignment_tag
def define(val=None):
    return val

@register.filter
def get_form(name):
    if name:
        form=StoreKeeperForm(initial={'name':name})
    else:
        form=StoreKeeperForm()
    return form['name']

@register.filter
def get_absolute_value(name):
    if name:
        return str(name)+' ('+str(name.Room_Number)+')'
    else:
        return '-'