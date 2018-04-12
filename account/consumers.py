# In consumers.py
from channels import Group,Channel
from channels.sessions import channel_session
from channels.asgi import get_channel_layer
import json

@channel_session
def ws_connect(message):    
    message.reply_channel.send({'accept': True})
    if message.content['query_string'].decode() == 'apikey=master':
        Group("headClient").add(message.reply_channel)


@channel_session
def ws_message(message):
    try:
        if get_channel_layer().group_channels('headClient'):
            get_channel_layer().group_channels('headClient')[message.content['reply_channel']]
            Channel(json.loads(message.get('text'))['reply_channel']).send({'text':
                                                                        json.dumps(json.loads(message.get('text'))['message'])},immediately=True)
        else:
            message.reply_channel.send({'text':'Head client not found'})
    except:
        Group("headClient").send({'text': json.dumps(
            {'reply_channel': message.content['reply_channel'], 'message': message.get('text')})}, immediately=True)

@channel_session
def ws_disconnect(message):
    Group("headClient").discard(message.reply_channel)
    message.reply_channel.send({'close':True})
