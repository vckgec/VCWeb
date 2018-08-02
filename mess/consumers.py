# In consumers.py
import json
from datetime import date
from channels import Group
from django.db.models import Q
from mess.models import Store, MealDish
from channels.sessions import channel_session

# Connected to websocket.connect
@channel_session
def ws_connect(message):    
    message.reply_channel.send({'accept': True})
    # Work out room name from path (ignore slashes)
    #room = message.content['path'].strip("/")
    # Save room in session and add us to the group
    #message.channel_session['room'] = room
    Group("mess").add(message.reply_channel)


# Connected to websocket.receive
@channel_session
def ws_message(message):
    meal_today=Store.objects.filter(date=date.today(),half=json.loads(message.get('text'))['half'])
    if meal_today:
        meal={}
        id_meal = MealDish.objects.filter(Q(dish__contains='BIRIYANI') | Q(dish__contains='ID'), date__gte=date.today()).first()
        if id_meal:
            meal['id']={'id_date':str(id_meal.date),'id_half':id_meal.get_half()}                
        else:
            meal['id']={'id_date':None,'id_half':None}
        meal['dish'] = meal_today[0].meal_dish.dish
        meal['presence_count']=str(meal_today[0].presence.count())
        meal['half']=meal_today[0].get_half()
        meal['extra_meals']=str(meal_today[0].extra_meals)
        meal['non_count']=meal_today[0].get_absolute_string()
        meal['total_count']=str(meal_today[0].get_total_meals())
        Group("mess").send({'text':json.dumps(meal)})


# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    Group("mess").discard(message.reply_channel)
