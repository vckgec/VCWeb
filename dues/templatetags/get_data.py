from django import template
from account.models import Boarder
register = template.Library()


@register.filter(name='getName')
def name(field):
    if field.attname == 'id':
        return None
    else:
        return field.attname.replace('_', ' ').upper()

@register.filter(name='getValue')
def value(due, field):
    if field.attname == 'id':
        return None
    if field.attname=='name_id':
        return Boarder.objects.get(pk=due[field.attname])
    return due[field.attname]


@register.filter(name='getTotal')
def total(due,field=None):
    if field:
        if field=='Net':
            return Boarder.objects.get(pk=due['name_id']).dues.getTotalNet()
        if field=='Mess':
            return Boarder.objects.get(pk=due['name_id']).dues.getTotalMess()
    else:
        return Boarder.objects.get(pk=due['name_id']).dues.getTotal()