import datetime
import calendar
from .forms import *
from .models import *
from django.db.models import F,Q
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import messmanager_required, mess_member_required

def index(request):
    meal_today = Store.objects.filter(date=datetime.date.today())
    changeform = ChangeForm()
    mealform = MealForm()
    id_date=None
    id_half=None
    id_meal = MealDish.objects.filter(Q(dish__contains='BIRIYANI') | Q(dish__contains='Id'),date__gte=datetime.date.today()).first()
    if id_meal:
        id_date = id_meal.date
        id_half = id_meal.get_half()
    if request.user.is_authenticated:
        presence=Presence.objects.filter(boarder=request.user.boarder, date=datetime.date.today())
        status_mo = presence.get(half='1MO').get_status() if presence.filter(half='1MO') else 'unchecked'
        status_ev = presence.get(half='2EV').get_status() if presence.filter(half='2EV') else 'unchecked'
        context = {'status_mo': status_mo, 'status_ev':status_ev, 'changeform': changeform, 'mealform': mealform, 'meals_today': meal_today, 'id': {'id_date': id_date, 'id_half': id_half}}
    else:
        context = {'changeform': changeform, 'mealform': mealform,'meals_today': meal_today}
    return render(request, 'mess/mess.html', context)


def storeUpdate(request):
    half = request.POST['half']
    store = Store.objects.filter(date=datetime.datetime.today(), half=half)
    if store:       
        if not request.user.boarder.Current_Boarder:
            if request.POST['status'] =='off':
                store.update(extra_meals = F('extra_meals')-Presence.objects.filter(boarder=request.user.boarder,half=half ,date=datetime.datetime.today()).count())
            else:   
                store.update(extra_meals=F('extra_meals')+Presence.objects.filter(boarder=request.user.boarder, half=half, date=datetime.datetime.today()).count())
        else:
            if request.POST['status'] == 'off':
                store[0].presence.remove(*Presence.objects.filter(boarder=request.user.boarder, half=half ,date=datetime.datetime.today()))
            else:
                store[0].presence.add(*Presence.objects.filter(boarder=request.user.boarder, half=half, date=datetime.datetime.today()))
    return HttpResponse(half)


@login_required
def changeStatus(request):
    if request.method == 'POST':
        date=request.POST['date'] if 'date' in request.POST else datetime.date.today()
        time = {'1MO': 7, '2EV': 17}
        name = {'1MO': 'morning', '2EV': 'evening'}
        
        id_meal = MealDish.objects.filter(Q(dish__contains='BIRIYANI') | Q(dish__contains='ID'),date=date,half=request.POST['half']).first()
        if id_meal:
            if (datetime.datetime.combine(id_meal.date,datetime.time())-datetime.datetime.now()).days <= 0:
                if not str(datetime.date.today()) == str(date):
                    return HttpResponse('Can\'t change, as id time is less than 24 hours')
                else:
                    if datetime.datetime.now().hour < time[request.POST['half']]:
                        return HttpResponse('Can\'t change %s status after %s:00' % (name[request.POST['half']], time[request.POST['half']]))
                
        if str(datetime.date.today()) == str(date):            
            if datetime.datetime.now().hour < time[request.POST['half']]:
                Presence.objects.update_or_create(defaults={'status':request.POST['status']}, boarder=request.user.boarder, date=date, half=request.POST['half'])
            else: 
                return HttpResponse('Can\'t change %s status after %s:00' % (name[request.POST['half']], time[request.POST['half']]))
            return storeUpdate(request)
        else:
            Presence.objects.update_or_create(defaults={'status': request.POST['status']},boarder=request.user.boarder, date=date, half=request.POST['half'])
            return HttpResponse('Success')


@mess_member_required
def mealDish(request):  # meal import in MealDish model
    print('hi')
    if request.method == 'POST':
        temp={}
        temp['dish'] = request.POST['dish'].upper()
        if temp['dish'].find("BIRIYANI") != -1 or temp['dish'].find("ID") != -1:
            temp['has_chicken']=True
            temp['has_mutton']=True
        else:
            if temp['dish'].find("CHICKEN") != -1:
                temp['has_chicken'] = True
            else:
                temp['has_chicken'] = False

            if temp['dish'].find("MUTTON") != -1:
                temp['has_mutton'] = True
            else:
                temp['has_mutton'] = False
        if temp['dish'].find("FISH") != -1 or temp['dish'].find("MACH") != -1:
            temp['has_fish'] = True
        else:
            temp['has_fish']=False

        if temp['dish'].find("EGG")!=-1 or temp['dish'].find("DIM")!=-1:
            temp['has_egg']=True
        else:
            temp['has_egg']=False

        MealDish.objects.update_or_create(defaults=temp,date=request.POST['date'], half=request.POST['half'])
        return HttpResponse(request.POST['half'])


@login_required
def guestMeal(request):  # guest meal dtails wil be input from user
    if request.method == 'POST':
        guestform = GuestForm(request.POST)
        if guestform.is_valid():
            number = guestform.cleaned_data.pop('number')
            obj,created=GuestMeal.objects.update_or_create(defaults={'number':number},boarder=request.user.boarder, **guestform.cleaned_data)
            if created:
                store = Store.objects.filter(date=guestform.cleaned_data['date'], half=guestform.cleaned_data['half']).first()
                if store:
                    store.guest_meal.add(obj)
            messages.success(request, 'Guest meal successfully added')
            return redirect('mess:home')
    else:
        guestform = GuestForm()
        return render(request, 'mess/guestmeal.html', {'guestform': guestform})


@messmanager_required
def extraAdjustment(request):  # Extra_mal and adjustmentcount, control by mess manager
    if request.method == 'POST':
        forms = [ExtraMealForm(request.POST),AdjustCountForm(request.POST)]
        field = {'ExtraMealForm': 'extra_meals', 'AdjustCountForm': 'adjust_count'}
        for form in forms:
            if form.is_valid():
                store = Store.objects.filter(date=date.today(), half=form.cleaned_data['half'])
                if store:
                    store.update(**{field[form.__class__.__name__]:form.cleaned_data[field[form.__class__.__name__]]})
                    messages.success(request, '%s has been added'%field[form.__class__.__name__].replace('_',' ').capitalize())
        return redirect('mess:home')
    else:
        forms = [ExtraMealForm(), AdjustCountForm()]
        return render(request, 'mess/extraadjustment.html', {'forms': forms})

@login_required
def storeKeeper(request):
    second_year=StoreKeeper.objects.filter(date__month=datetime.datetime.now().month).order_by('date','half')
    return render(request,'mess/storekeeper.html',{'juniors':second_year})


@login_required
def storeKeeperEdit(request):
    now = datetime.datetime.now()
    second_year = StoreKeeper.objects.filter(date__month=now.month).order_by('date', 'half')
    if request.method == 'POST':
        half = ['1MO', '2EV']
        data = request.POST.getlist('name')
        for i in range(calendar.monthrange(now.year, now.month)[1]):
            for j in range(2):
                StoreKeeper.objects.update_or_create(defaults={'name_id':data[2*i+j]},date=datetime.datetime(now.year, now.month, i+1).date(), half=half[j])
        messages.success(request, "Successfully submitted data")
        return redirect('mess:storekeeper')
    return render(request, 'mess/storekeeperedit.html', {'juniors': second_year})