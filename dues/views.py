from django.shortcuts import render
from .forms import PrintScan
from account.models import Boarder
from.models import *
from django.db.models import Count,Max
# Create your views here.

def index(request):
    #fields=['Name','First charge','Net','Print & Scan','Canteen','Recreation','Mess','Mess Bill']
    fields=Dues._meta.fields
    dues = Dues.objects.all().values().annotate(Year_Of_Passing=Max(
        'name__Year_Of_Passing')).order_by('-Year_Of_Passing')
    print(Dues.objects.all().values().annotate(Year_Of_Passing=Max('name__Year_Of_Passing')).order_by('-Year_Of_Passing'))
    return render(request,'dues/dues.html',{'fields':fields,'dues':dues})

def printScan(request):
    if request.POST:
        form=PrintScan(request.POST)
        if form.is_valid():
            cost = {'a4_paper': 0.40, 'bw_print_single': 0.80, 'bw_print_double': 1.20,
                    'color_print': 4.00, 'five_photo_strip': 20.00, 'photo_paper': 100.00}
            total_cost=0
            for key,value in cost.items():
                total_cost += value*float(form.cleaned_data[key]) if form.cleaned_data[key] else 0
            dues=Dues.objects.filter(name=Boarder.objects.get(pk=form.cleaned_data['user']))
            if dues:                
                dues[0].print_scan += total_cost
                dues[0].save()
            else:
                Dues.objects.create(name=Boarder.objects.get(
                    pk=form.cleaned_data['user']), print_scan=total_cost)
    else:
        form=PrintScan()
    return render(request,'dues/printscan.html',{'form':form})