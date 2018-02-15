from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response
from django.template import loader
from django.contrib import messages
from datetime import datetime
import calendar
from .models import *
from django.db.models import Min,Max
from account.models import *
from .forms import *
import arrow
import time
import threading
#from weasyprint import HTML

# Create your views here.


def Decrypt(status):
    if status==True or status=="on":
        return 'checked'
    else:
        return 'unchecked'

#def gen(xxx,yyy):
    #lenth=len(yyy)
    #yyy=yyy[-1]+yyy+yyy[0]
    #veg=0
    #for i in range(lenth):
        #veg+=(xxx[yyy[i+1]]-xxx[yyy[i:i+2]]-xxx[yyy[i+1:i+3]]+xxx[yyy[i:i+3]])+(xxx[yyy[i+1:i+3]]-xxx[yyy[i:i+3]]-xxx[yyy[i+1:i+4]]+xxx[yyy[1:lenth+1]])+(xxx[yyy[i+1:i+4]]-xxx[yyy[1:lenth+1]])
    #veg+=xxx[yyy[1:lenth+1]]
    #return veg
    #temp={}
    #temp['312']=temp['123']=5
    #temp['231']=5
    #temp['31']=10
    #temp['12']=10
    #temp['23']=10
    #temp['1']=20
    #temp['2']=20
    #temp['3']=20
    #print(gen(temp,'123'))

def Home(request):
    boarder=Boarder.objects.filter(user=request.user.id)
    meal_today=Presence.objects.filter(meal_date=date.today())
    changeform = ChangeForm()
    mealform = MealForm()
    guestform=GuestForm()
    if MealDishes.objects.all():
        last_meal=MealDishes.objects.latest('Meal_Date')
        if last_meal.Meal_Date >= date.today():
            if last_meal.Meal_Dish.lower().find("biriyani")!=-1 or last_meal.Meal_Dish.lower().find("id")!=-1:
                id_date=str(last_meal.Meal_Date)
                id_half=last_meal.Half()
            else:
                id_date=None
                id_half=None
        else:
            id_date=None
            id_half=None
    else:
        id_date=None
        id_half=None
    if boarder:
        context={'status_mo':Decrypt(boarder[0].Morning_Presence),'status_ev':Decrypt(boarder[0].Evening_Presence),'changeform':changeform,'mealform': mealform,'meals_today':meal_today,'id':{'id_date':id_date,'id_half':id_half}}
    else:
        context={'changeform':changeform,'mealform': mealform,'meals_today':meal_today,'id':id}
    return render(request,'mess/mess.html',context)

def Presence_Update(half): # after on/off status, this function will be invoke for presence update
    presence=Presence.objects.filter(meal_date=date.today(),half=half)
    if not presence:
        presence=Presence()
        presence.half=half
        presence.meal_date=date.today()
        presence.change_by=datetime.now()
        presence.save()
    presence=Presence.objects.get(meal_date=date.today(),half=half)
    if half=='MO':
        presence.boarder.remove(*Boarder.objects.filter(Morning_Presence=False,Presence_Date=date.today()))
        presence.boarder.add(*Boarder.objects.filter(Morning_Presence=True,Presence_Date=date.today()))
    else:
        presence.boarder.remove(*Boarder.objects.filter(Evening_Presence=False,Presence_Date=date.today()))
        presence.boarder.add(*Boarder.objects.filter(Evening_Presence=True,Presence_Date=date.today()))
    return HttpResponse(half)

@login_required
def Change_Current_Status(request): # for slider switch
    if request.method=='POST':
        boarder=Boarder.objects.get(pk=request.POST['username'])
        boarder.Presence_Date=date.today() #arrow.get(request.POST['date'],'MM/D/YYYY').format('YYYY-MM-DD')
        half=request.POST['half']
        if half=='MO':
            boarder.Morning_Presence=request.POST['status']
        else:
            boarder.Evening_Presence=request.POST['status']
        boarder.save()
    return Presence_Update(half)


def Meal_Update(half):  # after input meal_dish in the database, this func will invoke to update meal and other related option in presence
    presences=Presence.objects.filter(meal_date=date.today())
    if presences:
        for presence in presences:
            dish=MealDishes.objects.filter(Meal_Date=presence.meal_date,Meal_Half=presence.half)
            if dish:
                presence.meal_dishes=dish[0].Meal_Dish
                if dish[0].Meal_Dish.lower().find("biriyani")!=-1 or dish[0].Meal_Dish.lower().find("id")!=-1:
                    presence.has_chicken=True
                    presence.has_mutton=True

                    if dish[0].Meal_Dish.lower().find("fish")!=-1 or dish[0].Meal_Dish.lower().find("mach")!=-1:
                        presence.has_fish=True
                    else:
                        presence.has_fish=False

                    if dish[0].Meal_Dish.lower().find("egg")!=-1 or dish[0].Meal_Dish.lower().find("dim")!=-1:
                        presence.has_egg=True
                    else:
                        presence.has_egg=False
                else:
                    presence.has_chicken=False
                    presence.has_mutton=False

                    if dish[0].Meal_Dish.lower().find("fish")!=-1 or dish[0].Meal_Dish.lower().find("mach")!=-1:
                        presence.has_fish=True
                    else:
                        presence.has_fish=False

                    if dish[0].Meal_Dish.lower().find("chicken")!=-1:
                        presence.has_chicken=True
                    else:
                        presence.has_chicken=False

                    if dish[0].Meal_Dish.lower().find("mutton")!=-1:
                        presence.has_mutton=True
                    else:
                        presence.has_mutton=False

                    if dish[0].Meal_Dish.lower().find("egg")!=-1 or dish[0].Meal_Dish.lower().find("dim")!=-1:
                        presence.has_egg=True
                    else:
                        presence.has_egg=False
                presence.save()
    return HttpResponse(half)

@login_required
def Meal_Dish(request): # meal import in meal_dish model
    if request.method == 'POST':
        dish=MealDishes.objects.filter(Meal_Date=request.POST['date'],Meal_Half = request.POST['half'])
        if not dish:
            dish=MealDishes()
            dish.Meal_Dish = request.POST['meal']
            dish.Meal_Half = request.POST['half']
            dish.Meal_Date = request.POST['date']
            dish.save()
        else:
            dish[0].Meal_Dish = request.POST['meal']
            dish[0].save()
    return Meal_Update(request.POST['half'])


def StoreKeeper_Create():    # Every month this will update StoreKeeper model
    now = datetime.now()
    store=StoreKeeper.objects.filter(Store_Date__month=now.month)
    if not store:
        try:
            if calendar.monthrange(now.year, now.month)[1]<=calendar.monthrange(now.year, now.month-1)[1]:
                store=StoreKeeper.objects.filter(Store_Date__month=now.month-1).order_by('Store_Date','Store_Half')
            else:
                store=StoreKeeper.objects.filter(Store_Date__month=now.month-2).order_by('Store_Date','Store_Half')
        except:
            pass
        Half=['1MO','2EV']
        for i in range(2*calendar.monthrange(now.year, now.month)[1]):
            store_object=StoreKeeper()
            store_object.Store_Date=datetime(now.year, now.month, int(i/2+1)).date()
            try:
                store_object.Store_Half=store[i].Store_Half
                store_object.Store_Name=store[i].Store_Name
            except:
                store_object.Store_Name=None
                store_object.Store_Half=Half[i%2]
            store_object.save()
    return Meal_Update("Success")



def Presence_Create(): # Every day at 00:00 it will create MO and EV presence of current date in presence model
    presences=Presence.objects.filter(meal_date=date.today())
    if not presences:
        presence_ev=Presence()
        presence_ev.half='EV'
        presence_ev.meal_date=date.today()
        presence_ev.change_by=datetime.now() 
        presence_ev.save()
        presence_ev.boarder.add(*Boarder.objects.filter(Evening_Presence=True,Presence_Date=date.today()))
        presence_mo=Presence()
        presence_mo.half='MO'
        presence_mo.meal_date=date.today()
        presence_mo.change_by=datetime.now()
        presence_mo.save()
        presence_mo.boarder.add(*Boarder.objects.filter(Morning_Presence=True,Presence_Date=date.today()))
        presences=Presence.objects.filter(meal_date=date.today())
        for presence in presences:
            guestscount=GuestMeal.objects.filter(Meal_Date=date.today(),Meal_Half=presence.half)
            if guestscount:
                count=0
                for guestcount in guestscount:
                    count+=guestcount.No_Of_Guest
                presence.guest_meal=count
                presence.save()
        return StoreKeeper_Create()
    else:
        return "Already Created"


def Boarder_Update(): # Every day at 00:00 it will update what will be the boarder MO and EV status for that day
    threading.Timer(60.0, Boarder_Update).start()
    presence=Presence.objects.filter(meal_date=date.today())
    if not presence:
        boarders=Boarder.objects.all()
        for boarder in boarders:
            if boarder.Evening_Presence:
                boarder.Morning_Presence=True
                boarder.Presence_Date=date.today()
                boarder.save()
                updateboarder=FutureBoarder.objects.filter(user=boarder.user,offdate=date.today(),offhalf='MO')
                if updateboarder:
                    boarder.Morning_Presence=False
                    boarder.save()
                if not boarder.Morning_Presence:
                    boarder.Evening_Presence=False
                    boarder.save()
                updateboarder=FutureBoarder.objects.filter(user=boarder.user,ondate=date.today(),onhalf='EV')
                if updateboarder:
                    boarder.Evening_Presence=True
                    boarder.save()
            else:
                boarder.Morning_Presence=False
                boarder.Presence_Date=date.today()
                boarder.save()
                updateboarder=FutureBoarder.objects.filter(user=boarder.user,ondate=date.today(),onhalf='MO')
                if updateboarder:
                    boarder.Morning_Presence=True
                    boarder.save()
                if boarder.Morning_Presence:
                    boarder.Evening_Presence=True
                updateboarder=FutureBoarder.objects.filter(user=boarder.user,offdate=date.today(),offhalf='EV')
                if updateboarder:
                    boarder.Evening_Presence=False
                    boarder.save()
        return Presence_Create()
    else:
        return "Already Updated"

@login_required
def Future(request): # save on/off status in this model
    if request.method=='POST':
        futureboarder=FutureBoarder.objects.filter(user=request.user.id)
        if not futureboarder:
            future=FutureBoarder()
            future.user=User.objects.get(id=request.user.id)
            future.ondate=date.today()
            
            future.onhalf=request.POST['half']
            future.offdate=date.today()
            future.offhalf=request.POST['half']
            future.save()
        futureboarder=FutureBoarder.objects.get(user=request.user.id)
        if request.POST['status']=='on':
            futureboarder.ondate=request.POST['date']
            futureboarder.onhalf=request.POST['half']
        else:
            futureboarder.offdate=request.POST['date']
            futureboarder.offhalf=request.POST['half']
        futureboarder.save()
    return JsonResponse({'date':request.POST['date'],'half':request.POST['half'],'status':Decrypt(request.POST['status'])})

@login_required
def guestmeal(request): # guest meal dtails wil be input from user
    if request.method == 'POST':
        guestform=GuestForm(request.POST)
        if guestform.is_valid():
            guest=GuestMeal.objects.filter(user=request.user,Meal_Date=guestform.cleaned_data['Meal_Date'],Meal_Half=guestform.cleaned_data['Meal_Half'])
            if guest:
                guest[0].No_Of_Guest=guestform.cleaned_data['No_Of_Guest']
                guest[0].save()
            else:
                req=guestform.save(commit=False)
                req.user=request.user
                req.save()
            messages.success(request, 'Guest meal successfully added')
            presence=Presence.objects.get(meal_date=date.today(),half=guestform.cleaned_data['Meal_Half'])
            guestscount=GuestMeal.objects.filter(Meal_Date=date.today(),Meal_Half=guestform.cleaned_data['Meal_Half'])
            if guestscount:
                count=0
                for guestcount in guestscount:
                    count+=guestcount.No_Of_Guest
                presence.guest_meal=count
                presence.save()
            return redirect('mess:home')
    else:
        guestform=GuestForm()
        return render(request,'mess/guestmeal.html',{'guestform':guestform})

@login_required
def ExtraAdjustment(request): # Extra_mal and adjustmentcount, control by mess manager
    if request.method == 'POST':
        extraform=ExtraMealForm(request.POST)
        adjustform=AdjustCountForm(request.POST)
        if extraform.is_valid():
            presence=Presence.objects.filter(meal_date=date.today(),half=extraform.cleaned_data['half'])
            if presence:
                presence[0].extra_meals=extraform.cleaned_data['extra_meals']
                presence[0].save()
            messages.success(request, 'Extra meal has been added')
            return redirect('mess:home')
        if adjustform.is_valid():
            presence=Presence.objects.filter(meal_date=date.today(),half=adjustform.cleaned_data['half'])
            if presence:
                presence[0].adjust_count=adjustform.cleaned_data['adjust_count']
                presence[0].save()
            messages.success(request, 'Adjust count successfully added')
            return redirect('mess:home')
    else:
        extraform=ExtraMealForm()
        adjustform=AdjustCountForm()
        return render(request,'mess/extraadjustment.html',{'extraform':extraform,'adjustform':adjustform})

@login_required
def Store_Keeper(request):
    second_year=StoreKeeper.objects.filter(Store_Date__month=datetime.now().month).order_by('Store_Date','Store_Half')
    return render(request,'mess/storekeeper.html',{'juniors':second_year})

@login_required
def Store_Keeper_Edit(request):
    now = datetime.now()
    second_year=StoreKeeper.objects.filter(Store_Date__month=now.month).order_by('Store_Date','Store_Half')
    if request.method=='POST':
        data=request.POST.getlist('Store_Name')
        for i in range(calendar.monthrange(now.year, now.month)[1]):
            store=StoreKeeper.objects.filter(Store_Date=datetime(now.year, now.month, i+1).date())
            try:
                morning_store=store.get(Store_Half='1MO')
            except:
                morning_store=StoreKeeper()
                morning_store.Store_Date=datetime(now.year, now.month, i+1).date()
                morning_store.Store_Half='1MO'
            morning_store.Store_Name=Boarder.objects.get(id=data[2*i])
            morning_store.save()

            try:
                evening_store=store.get(Store_Half='2EV')
            except:
                evening_store=StoreKeeper()
                evening_store.Store_Date=datetime(now.year, now.month, i+1).date()
                evening_store.Store_Half='2EV'
            evening_store.Store_Name=Boarder.objects.get(id=data[2*i+1])
            evening_store.save()
        messages.success(request,"Successfully submitted data")
        return redirect('mess:storekeeper')
    return render(request,'mess/storekeeperedit.html',{'juniors':second_year})


#def html_to_pdf_view(request):
    #second_year=StoreKeeper.objects.filter(Store_Date__month=datetime.now().month).order_by('Store_Date','Store_Half')
    #html_string = render_to_string('mess/storekeeper.html',{'juniors':second_year})

    #html = HTML(string=html_string)
    #html.write_pdf(target='/tmp/mypdf.pdf');

    #fs = FileSystemStorage('/tmp')
    #with fs.open('mypdf.pdf') as pdf:
        #response = HttpResponse(pdf, content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        #return response

    #return response

def web(request):
    from pip._vendor import requests
    import bs4
    url="http://192.168.0.110:8080/mess/storekeeperedit"
    #print("downloading page ", url)
    res = requests.get(url)
    #print(res)
    res.raise_for_status()
    #soup = bs4.BeautifulSoup(res.text, "lxml")
    return HttpResponse(res.text)