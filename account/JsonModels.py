import os
import json
import collections
from django.apps import apps
from django.core import serializers
from django.contrib.auth.models import User

class JSON: 
    models=collections.OrderedDict()
    filename=None

    #constructror overloading
    def __init__(self,appname=None,filename=None):
        self.models=apps.all_models[appname]
        self.filename=filename
        for keys,value in self.models.items():
            print(keys,value)


    def JsonDump(self,table=None):
        if not table:
            for key , value in self.models.items():
                data = serializers.serialize("json", value.objects.all())
                write=open(os.getcwd().replace('\\','/')+'/'+key+'.json','w')
                write.write(data)
                write.close()
        else:
            if table in self.models.items():
                data = serializers.serialize("json", self.models[table].objects.all())
                
            else:
                if table.lower()=='user':
                    data = serializers.serialize("json", User.objects.all())
            write=open(os.getcwd().replace('\\','/')+'/'+table+'.json','w')
            write.write(data)
            write.close()

    def JsonLoad(self,table=None):
        if self.filename and not table:
            read=open(self.filename,'r')
        else:
            read=open(os.getcwd().replace('\\','/')+'/'+table+'.json','r')
        data=serializers.deserialize('json', read.read(), ignorenonexistent=True)
        for obj in data:
            obj.save()