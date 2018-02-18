import os
import json
import collections
from django.apps import apps
from django.core import serializers
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

class JSON: 
    models=collections.OrderedDict()
    files=None
    def __init__(self,app=None,files=None):
        if app!='all':        
            self.models=apps.all_models[app]
        else:
            for value in apps.all_models.values():
                self.models.update(value)
        self.files=files

    def JsonDump(self,table=None):
        if not table:
            write=[]
            for key,value in self.models.items():
                data = serializers.serialize("json", value.objects.all())
                write.append({'filename':key,'filecontent':ContentFile(data)})
                '''write=open(os.getcwd().replace('\\','/')+'/'+key+'.json','w')
                write.write(data)
                write.close()'''
            
        else:
            if table in self.models.items():
                data = serializers.serialize("json", self.models[table].objects.all())
            write=open(os.getcwd().replace('\\','/')+'/'+table+'.json','w')
            write.write(data)
            write.close()
        return write

    def JsonLoad(self,table=None):
        reads=[]
        if self.files and not table:
            for file in self.files:
                reads.append(open(file,'r'))
        else:
            if table:
                reads.append(open(os.getcwd().replace('\\','/')+'/'+table+'.json','r'))
        for read in reads:
            objs=serializers.deserialize('json', read.read(), ignorenonexistent=True)
            for obj in objs:
                obj.save()