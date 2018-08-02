from django import template
from django.db.models import Sum
from account.models import Boarder
from committee.models import Account,Committee
register = template.Library()


@register.filter(name='get')
def attr(field,index):  # attr=(x,y)
    return field[index]


@register.filter(name='total')
def total(accounts,attr):
    return sum(getattr(account,attr) for account in accounts)


@register.filter(name='whole')
def whole(committee, attr):
    return Account.objects.filter(committee=committee).aggregate(val=Sum(attr))['val']


@register.filter(name='balance')
def current_bal(log):
    accounts = Account.objects.filter(pk__in=list(range(log.pk+1)), committee=log.committee, changed_by=log.changed_by)
    return accounts.aggregate(balance=Sum('credit')-Sum('debit'))['balance']


@register.filter(name='Name')
def get_baoarder_name(id):
    return Boarder.objects.filter(id=id).first().Name


@register.assignment_tag
def define():
    return Committee.NAME_CHOICES


@register.filter()
def getType(path):
    import re
    return re.sub('/[a-z]+/[a-z]+|/', '', path)
