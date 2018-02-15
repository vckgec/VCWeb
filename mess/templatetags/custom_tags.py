from django import template
from mess.forms import StoreKeeperForm
register = template.Library()

@register.filter(name='sort')
def sort_by(queryset): #we can also use inbuild tag {% for meal in meal_today|dictsort:"get_current_half" %}--------look mess/mess.html
    if queryset[0].get_current_half() == 1:
        return queryset
    else:
        new_set=[]
        for i in range(1,-1,-1):
            new_set.append(queryset[i])
    return new_set

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
        form=StoreKeeperForm(initial={'Store_Name':name})
    else:
        form=StoreKeeperForm()
    return form['Store_Name']

@register.filter
def get_absolute_value(name):
    if name:
        return str(name)+' ('+str(name.Room_Number)+')'
    else:
        return '-'