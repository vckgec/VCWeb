from functools import wraps
from .models import Committee
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def commiteee_required(function=None, name=None):
    if not function:
        def check_required(func):
            @wraps(func)
            @login_required
            def wrapper(*args, **kwargs):
                nonlocal name
                if kwargs:
                    for value in kwargs.values():
                        name = value
                name=name.replace('messbill','mess')
                required_committee = Committee.objects.filter(name=name, members=args[0].user.boarder)
                if required_committee:
                    return func(*args, **kwargs)
                else:
                    messages.warning(args[0], 'Current user is not %s committee' % name)
                    return redirect('%s:home' % args[0].resolver_match.app_name)
            return wrapper
        return check_required
    else:
        @wraps(function)
        @login_required
        def wrapper(*args, **kwargs):
            nonlocal name
            for value in kwargs.values():
                name = value
            name = name.replace('messbill', 'mess')
            required_committee = Committee.objects.filter(name=name, members=args[0].user.boarder)
            if required_committee:
                return function(*args, **kwargs)
            else:
                messages.warning(args[0], 'Current user is not a member of %s committee' % name)
                return redirect('%s:home' % args[0].resolver_match.app_name)
        return wrapper