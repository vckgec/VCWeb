from .models import Committee
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin

class CommitteeRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        else:
            if Committee.objects.filter(name=self.committe, members=request.user.boarder):
                return super(CommitteeRequiredMixin, self).dispatch(request, *args, **kwargs)
            else:
                messages.warning(request,'Current user not in %s committee' %self.committe)
                return redirect('%s:home' % request.resolver_match.app_name)
