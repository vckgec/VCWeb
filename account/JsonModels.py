import os
import json
import collections
from django.apps import apps
from django.core import serializers
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import re,datetime

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
                # if key=='book':
                #     f=open('xx.json','w')
                #     f.write(data)
                #     f.close()
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

    def JsonLoad(self,dbtype,table=None):
        read={}
        if self.files and not table:
            for file in self.files:
                if dbtype=='sqllite':
                    json_data=open(file,'r').read()
                    read[json.loads(json_data)[0]['model'].split('.')[1]]=json_data
                else:
                    json_data=json.loads(open(file,'r').read())
                    read[json_data[0]['model'].split('.')[1]]=json_data
        else:
            if table:
                if dbtype=='sqllite':
                    json_data=open(os.getcwd().replace('\\','/')+'/'+table+'.json','r').read()
                    read[json.loads(json_data)[0]['model'].split('.')[1]]=json_data
                else:
                    json_data=json.loads(open(os.getcwd().replace('\\','/')+'/'+table+'.json','r').read())
                    read[json_data[0]['model'].split('.')[1]]=json_data

                
        if dbtype=='sqllite':
            for value in read.values():
                objs=serializers.deserialize('json', value, ignorenonexistent=True)
                for obj in objs:
                    obj.save()

        else:


            completed=0
            missing_objects=0
            while len(read)>completed:
                for key, value in read.items():
                    if self.models[key].objects.count() < len(read[key])-missing_objects:#not self.models[key].objects.all():
                        for field in self.models[key]._meta.fields:
                            if field.is_relation:
                                if field.related_model._meta.model_name in read.keys():
                                    if field.related_model.objects.count() >= len(read[field.related_model._meta.model_name]):
                                        for i in range(len(value)):
                                            for related_model_obj in read[field.related_model._meta.model_name]:
                                                if value[i]['fields'][field.name] == related_model_obj['pk']:
                                                    for related_model_field in field.related_model._meta.fields:
                                                        if related_model_field.is_relation:
                                                            try:
                                                                del related_model_obj['fields'][related_model_field.name]
                                                            except:
                                                                pass # Already deleted for that object
                                                    value[i]['fields'][field.name] = field.related_model.objects.get(**related_model_obj['fields'])
                                        is_ready=True
                                    else:
                                        is_ready=False
                                        break #for next time making it as model, not related model
                                else:
                                    if field.related_model.objects.all():
                                        for i in range(len(value)):
                                            try:
                                                value[i]['fields'][field.name]=field.related_model.objects.get(pk=value[i]['fields'][field.name])
                                            except Exception as e:
                                                pass #matching query does not exist
                                        is_ready=True
                                        print("Arrangement may be wrong due to missing of "+field.related_model._meta.model_name+".json")
                                    else:
                                        raise KeyError(field.related_model._meta.model_name+'.json missing')
                            else:
                                is_ready=True

                        if is_ready:                            
                            for obj in value:
                                for field in self.models[key]._meta.fields:
                                    if re.findall('Date[a-z?A-Z]*Field', field.get_internal_type()):
                                        try:
                                            obj['fields'][field.name]=datetime.datetime(*map(int, str(obj['fields'][field.name].split('-'))))
                                        except:
                                            pass # when value=None
                                try:
                                    if not self.models[key].objects.filter(**obj['fields']):                                        
                                        self.models[key].objects.create(**obj['fields'])
                                except Exception as e:
                                    print(e)
                                    missing_objects+=1
                    else:
                        completed+=1






























                        


            '''
            //////////////////////for user model only ///////////////////////
            for key,value in read.items():
                for item in value:
                    temp={}
                    temp['username']=item['fields']['username']
                    temp['password']=item['fields']['password']
                    us=User(**temp)
                    us.save()'''

            # control=0
            # while len(read)>control:
            #     for key,value in read.items():
            #         if not self.models[key].objects.all():
            #             dependent_model_fields=[]                        
            #             for field in self.models[key]._meta.fields:
            #                 if field.name in self.models.keys():
            #                     dependent_model_fields.append(field)
            #             if len(dependent_model_fields)>0:
            #                 is_modify=False
            #                 for field in dependent_model_fields:
            #                     if field.name not in read.keys():
            #                         if not self.models[field.name].objects.all():
            #                             raise KeyError(field.name+'.json does not exist')
            #                         else:
            #                             pass
            #                     else:
            #                         if self.models[field.name].objects.all():
            #                             for i in range(len(value)):
            #                                 for independ in read[field.name]:
            #                                     deleted_fild={}
            #                                     if value[i]['fields'][field.name]==independ['pk']:
            #                                         independent_model_fields=[]
            #                                         for fild in self.models[field.name]._meta.fields:
            #                                             if fild.name in self.models.keys():
            #                                                 independent_model_fields.append(fild)
            #                                         for fild in independent_model_fields:
            #                                             deleted_fild[fild.name]=independ['fields'][fild.name]                                               
            #                                             del independ['fields'][fild.name]
            #                                         value[i]['fields'][field.name]=self.models[field.name].objects.get(**independ['fields'])                                                
            #                                         is_modify=True
            #                                         if deleted_fild:
            #                                             independ['fields'][fild.name]=deleted_fild[fild.name]   
            #                                         break
            #                         else:
            #                             independent_model_fields=[]
            #                             for fild in self.models[field.name]._meta.fields:
            #                                 if fild.name in self.models.keys():
            #                                     independent_model_fields.append(fild)
            #                             if len(independent_model_fields)<1:
            #                                 for totaly_independ in read[field.name]:
            #                                     self.models[field.name].objects.create(**totaly_independ['fields'])
            #                     if is_modify:
            #                         for depend in value:
            #                             self.models[key].objects.create(**depend['fields'])
            #             else:
            #                 for totaly_independ in value:
            #                     self.models[key].objects.create(**totaly_independ['fields'])
            #         if self.models[key].objects.count()==len(value):                    
            #             control+=1


            '''if len(reads)>1:
                re1=json.loads(reads[1].read())
                re0=json.loads(reads[0].read())
                for read1 in re1:#req
                    for read0 in re0:#book
                        if read1['fields']['book']==read0['pk']:
                            del read1['fields']['book']
                            print(read0['fields'])
                            sub=read0['fields']['subject']
                            del read0['fields']['subject']
                            print(read0['fields'])
                            req=Request(book=Book.objects.get(**read0['fields']),**read1['fields'])
                            req.save()
                            read0['fields']['subject']=sub
                            break
            else:
                re0=json.loads(reads[0].read())
                for read0 in re0:
                    try:
                        bk=User(**read0['fields'])
                        bk.save()
                    except:
                        pass'''