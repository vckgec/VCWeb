import calendar
import datetime
import threading
from .models import *
from django.db.models import Subquery
from dateutil.relativedelta import relativedelta


def storeCreate(half):
    for i in range(2):
        presence = Presence.objects.filter(date=datetime.date.today(), status='on', half=half[i])
        meal_dish = MealDish.objects.filter(date=datetime.date.today(), half=half[i]).first()
        guest_meal = GuestMeal.objects.filter(date=datetime.date.today(), half=half[i])
        mess_manager = MessManager.objects.filter(start__month=datetime.date.today().month,start__year=datetime.date.today().year).first()
        store_keeper = StoreKeeper.objects.filter(date=datetime.date.today(), half=half[i]).first()
        store = Store.objects.create(half=half[i],meal_dish=meal_dish,mess_manager=mess_manager,store_keeper=store_keeper)
        store.presence.add(*presence)
        store.guest_meal.add(*guest_meal)
    return 'Created'
                
def storeKeeperCreate(half):
    now = datetime.datetime.now()
    store_keeper=StoreKeeper.objects.filter(date__month=now.month)
    if not store_keeper:
        try:
            if calendar.monthrange(now.year, now.month)[1]<=calendar.monthrange(now.year, now.month-1)[1]:
                store_keeper=StoreKeeper.objects.filter(date__month=now.month-1).order_by('date','half')
            else:
                store_keeper=StoreKeeper.objects.filter(date__month=now.month-2).order_by('date','half')
        except:
            pass
        for i in range(2*calendar.monthrange(now.year, now.month)[1]):  #multiply by 2 bcz MO+EV
            try:
                value = {'half': store_keeper[i].half,'name':store_keeper[i].name}
            except:
                value = {'half': half[i % 2], 'name': None}
            StoreKeeper.objects.create(date=datetime.datetime(now.year, now.month, int(i/2+1)).date(),**value)
    return storeCreate(half)

def messManagerCreate(half):
    mess_manager=MessManager.objects.filter(start__month=datetime.date.today().month,start__year=datetime.date.today().year)
    if not mess_manager:
        MessManager.objects.create(start=datetime.date.today())
    return storeKeeperCreate(half)


def mealDishCreate(half):
    for i in range(2):
        meal_dish = MealDish.objects.filter(date=datetime.date.today(), half=half[i])
        if not meal_dish:
            MealDish.objects.create(date=datetime.date.today(), half=half[i])
    return messManagerCreate(half)

def presenceCreate():
    threading.Timer(60.0, presenceCreate).start()
    store = Store.objects.filter(date=datetime.date.today())
    if not store:
        half=['1MO','2EV']
        presence_objs = []
        for i in range(2):
            presence_today=Presence.objects.filter(half=half[i],date=datetime.date.today())
            previous_presence = Presence.objects.filter(half=half[1-i],date=datetime.date.today()-datetime.timedelta(days=1-i)).exclude(boarder__in=Subquery(presence_today.values('boarder'))).values('boarder','status')        
            for presence in previous_presence:
                presence_objs.append(Presence(boarder_id=presence['boarder'], date=datetime.date.today(), status=presence['status'], half=half[i]))
            Presence.objects.bulk_create(presence_objs)
        return mealDishCreate(half)
    else:
        return 'Already Created'
