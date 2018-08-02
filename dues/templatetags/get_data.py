from django import template
from dues.models import Dues
from django.db.models import Sum
from account.models import Boarder

register = template.Library()


@register.filter(name='getAttr')
def attr(field):  # attr=(x,y)
    return field[0]


@register.filter(name='getName')
def name(field): #attr=(x,y)
    return field[1]

@register.filter(name='getValue')
def value(dues, field):
    return sum(due.added-due.paid for due in dues if due.name==field[0])


@register.filter(name='getTotal')
def total(dues,field=None):
    if field:
        if field=='Net':
            return sum(due.added-due.paid for due in dues if due.name =='net' or due.name=='printscan')
        if field=='Mess':
            return sum(due.added-due.paid for due in dues if due.name == 'mess' or due.name == 'messbill')
    else:
        return sum(due.added-due.paid for due in dues)


@register.filter(name='abs')
def abs_filter(value):
    return abs(value)


@register.filter()
def getType(path):
    import re
    return re.sub('/[a-z]+/|/', '', path)


@register.assignment_tag
def define():
    return Dues.NAME_CHOICES

@register.filter(name='getCurrent')
def current_due(log):
    dues=Dues.objects.filter(pk__in=list(range(log.pk+1)), name=log.name,boarder=log.boarder)
    return dues.aggregate(due=Sum('added')-Sum('paid'))['due']

@register.filter(name='Name')
def get_baoarder_name(id):
    return Boarder.objects.filter(id=id).first().Name
