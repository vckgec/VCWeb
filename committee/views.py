from .forms import *
from .models import *
from django.shortcuts import render,redirect
from .decorators import commiteee_required

# Create your views here.

def index(request):
    accounts=Account.objects.order_by('committee__name','changed_by')    
    return render(request,'committee/committee.html',{'accounts':accounts})

def getLogs(request,committee):
    accounts=Account.objects.filter(committee__name=committee).order_by('committee__name','-id')
    return render(request, 'committee/logs.html', {'accounts': accounts})

def account(request, boarder_id):
    accounts = Account.objects.filter(changed_by_id=boarder_id).order_by('committee__name','-id')
    return render(request, 'committee/account.html', {'logs': accounts})

@commiteee_required
def manage(request,committee):
    if request.POST:
        forms = [CreditForm(request.POST), DebitForm(request.POST)]
        for form in forms:
            if form.is_valid():
                obj=form.save(commit=False)
                obj.committee=Committee.objects.get(name=committee)
                obj.changed_by=request.user.boarder
                obj.save()
        return redirect('committee:home')
    else:
        forms = [CreditForm(), DebitForm()]
    return render(request, 'committee/manage.html', {'forms':forms})
