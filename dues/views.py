from .forms import *
from .models import *
from django.shortcuts import render, redirect
from committee.models import Account,Committee
from committee.decorators import commiteee_required
# Create your views here.


def index(request):
    fields = Dues.NAME_CHOICES
    dues = Dues.objects.filter(boarder__Current_Boarder=True).order_by('-boarder__Year_Of_Passing', 'boarder__Name')
    return render(request, 'dues/dues.html',{'fields':fields,'dues':dues})

@commiteee_required(name='net')
def printScan(request):
    if request.POST:
        form = PrintScan(request.POST)
        if form.is_valid():
            cost = {'a4_paper': 0.40, 'bw_print_single': 0.80, 'bw_print_double': 1.20,
                    'color_print': 4.00, 'five_photo_strip': 20.00, 'photo_paper': 100.00}
            message = {'a4_paper': 'A4 Page:', 'bw_print_single:': 'B/W Print or Xerox(Singlde Side):', 'bw_print_double': 'B/W Print or Xerox(Double Side):',
                        'color_print': 'Color Print:', 'five_photo_strip': 'Photo Strip(5 Pics) Print:', 'photo_paper': 'Photo Paper Print:'}
            total_cost = 0
            cause = ''
            for key, value in cost.items():
                total_cost += value * float(form.cleaned_data[key]) if form.cleaned_data[key] else 0
                cause += (message[key]+str(form.cleaned_data[key])+';') if form.cleaned_data[key] else ''
            Dues.objects.create(boarder_id=form.cleaned_data['user'], name='printscan', remarks=cause[0:-1], added=total_cost,changed_by=request.user.boarder)
    else:
        form = PrintScan()
    return render(request, 'dues/printscan.html', {'form': form})

def updateAccount(request,form,name):
    if form.name == 'Paid':
        committee=Committee.objects.get(name=name.replace('bill',''))
        if 'boarder_id' in form.cleaned_data:
            Account.objects.create(changed_by=request.user.boarder,committee=committee,credit=form.cleaned_data['paid'],remarks='Paid by %s'%Boarder.objects.get(id=form.cleaned_data['boarder_id']))
        else:
            account_list = []
            for boarder in Boarder.objects.filter(Current_Boarder=True):
                account_list.append(Account(changed_by=request.user.boarder, committee=committee, credit=form.cleaned_data['paid'], remarks='Paid by %s'%boarder))
            Account.objects.bulk_create(account_list)

@commiteee_required
def manage(request, field):
    if request.POST:
        forms = [AddForm(request.POST),PaidForm(request.POST)]
        for form in forms:
            if form.is_valid():
                if form.cleaned_data['boarder_id'] != '0':
                    Dues.objects.create(name=field,changed_by=request.user.boarder,**form.cleaned_data)
                else:
                    form.cleaned_data.pop('boarder_id')
                    dues_list=[]                    
                    for boarder in Boarder.objects.filter(Current_Boarder=True):
                        dues_list.append(Dues(boarder=boarder, name=field, changed_by=request.user.boarder,**form.cleaned_data))                            
                    Dues.objects.bulk_create(dues_list)
                updateAccount(request,form,field)
        return redirect('dues:home')
    else:
        forms = [AddForm(),PaidForm()]
        return render(request, 'dues/manage.html', {'forms': forms})

def getLogs(request,boarder_id):
    dues = Dues.objects.filter(boarder_id=boarder_id).order_by('-name', '-id')
    return render(request, 'dues/logs.html',{'logs':dues})
