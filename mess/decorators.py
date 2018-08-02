import datetime
from .models import MessManager
from django.contrib import messages
from django.shortcuts import redirect
from committee.models import Committee

class messmanager_required(object):
    def __init__(self,func):
        self.func=func
    def __call__(self,*args,**kwargs):
        mess_manager=MessManager.objects.filter(name=args[0].user.boarder,start__month=datetime.date.today().month,start__year=datetime.date.today().year)
        if mess_manager:
            return self.func(*args,**kwargs)
        else:
            messages.warning(args[0],'Current user in not mess manager for this month of this year')
            return redirect('%s:home' % args[0].resolver_match.app_name)


class mess_member_required:
    def __init__(self,func):
        self.func=func
    def __call__(self, *args, **kwargs):
        if Committee.objects.filter(name='mess', members=args[0].user.boarder) or MessManager.objects.filter(name=args[0].user.boarder, start__month=datetime.date.today().month, start__year=datetime.date.today().year):
            return self.func(*args, **kwargs)
        else:
            messages.warning(args[0], 'Current user in a mess member')
            return redirect('%s:home' % args[0].resolver_match.app_name)
