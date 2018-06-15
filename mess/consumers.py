# In consumers.py
from channels import Group
from channels.sessions import channel_session
import json
from mess.models import Presence, MealDishes
from datetime import date
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
    meal_today=Presence.objects.filter(meal_date=date.today(),half=json.loads(message.get('text'))['half'])
    if meal_today:
        meal=[]
        temp_meal={}
        if MealDishes.objects.all():  #for marque tag
            last_meal=MealDishes.objects.latest('Meal_Date')
            if last_meal.Meal_Date >= date.today():
                if last_meal.Meal_Dish.lower().find("biriyani")!=-1 or last_meal.Meal_Dish.lower().find("id")!=-1:
                    temp_meal['id']={'id_date':str(last_meal.Meal_Date),'id_half':last_meal.Half()}
                else:
                    temp_meal['id']={'id_date':None,'id_half':None}
            else:
                temp_meal['id']={'id_date':None,'id_half':None}
        else:
            temp_meal['id']={'id_date':None,'id_half':None}
        temp_meal['boarder_count']=str(meal_today[0].boarder.count())
        temp_meal['meal_half']=meal_today[0].meal_half()
        temp_meal['meal_dishes']=meal_today[0].meal_dishes
        temp_meal['extra_meals']=str(meal_today[0].extra_meals)
        temp_meal['non_count']=meal_today[0].get_absolute_string()
        temp_meal['guest_meal']=str(meal_today[0].guest_meal)
        temp_meal['total_count']=str(meal_today[0].get_total_meals())
        meal.append(temp_meal)
    Group("mess").send({'text':json.dumps(meal)})
# Connected to websocket.disconnect

@channel_session
def ws_disconnect(message):
    Group("mess").discard(message.reply_channel)