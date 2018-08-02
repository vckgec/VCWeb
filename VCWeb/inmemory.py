from mess.updates import presenceCreate
from asgiref.inmemory import ChannelLayer
class MyChannelLayer(ChannelLayer):
    def __init__(self):
        presenceCreate()
        super(MyChannelLayer,self).__init__(capacity=10000000)