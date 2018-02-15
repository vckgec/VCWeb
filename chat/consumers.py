# In consumers.py
from channels import Group
from channels.sessions import channel_session
from django.contrib.auth.models import User
from chat.models import Chat
from mess.models import Boarder
from datetime import datetime,date
from django.utils.dateformat import DateFormat
import json
from django.core.files import File
from django.core.files.base import ContentFile

# Connected to websocket.connect


@channel_session
def ws_connect(message):
    message.reply_channel.send({'accept': True})
    # Work out room name from path (ignore slashes)
    #room = message.content['path'].strip("/")
    # Save room in session and add us to the group
    #message.channel_session['room'] = room
    Group("chat").add(message.reply_channel)

# Connected to websocket.receive


@channel_session
def ws_message(message):
    data=[]
    temp={}
    user=User.objects.get(username=json.loads(message.get('text'))['username'])
    temp['username']=user.username
    temp['dp']=user.boarder.dp.url
    temp['name']=str(user.boarder)
    temp['message']=json.loads(message.get('text'))['message']
    temp['time']=str(DateFormat(datetime.now()).format('g:i a'))
    if Chat.objects.all():
        if Chat.objects.latest('chat_datetime').chat_datetime.date()==date.today():
            temp['chat_datetime']=None
        else:
            temp['chat_datetime']=str(date.today())
    else:
        temp['chat_datetime']=str(date.today())
    data.append(temp)
    chat=Chat()
    chat.username=user
    chat.dp=user.boarder.dp.url
    chat.name=user.boarder
    chat.message=json.loads(message.get('text'))['message']
    chat.chat_datetime=datetime.now()
    chat.save()
    Group("chat").send({'text':json.dumps(data)})

# Connected to websocket.disconnect


@channel_session
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)