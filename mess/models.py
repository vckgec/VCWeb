from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.db.models import Min,Max
from account.models import Boarder
from django.utils import timezone
from datetime import date
from datetime import datetime


# Create your models here.

def generate_length_wise_string(string,string_list,length):
    for i in range(length):
        for j in range(len(string)):
            for k in range(i+j,len(string)-(length-i-1)):
                if string[j:i+j]+string[k:k+length-i] not in string_list:
                    string_list.append(string[j:i+j]+string[k:k+length-i])
    return string_list

def get_value(data):
    
    return get_value

def get_string(string):
    temp={}
    temp['1']='Non Mutton: '
    temp['2']='Non Chicken: '
    temp['3']='Non Fish: '
    temp['4']='Non Egg: '
    temp['12']='Non Mutton and Chicken: '
    temp['13']='Non Mutton and Fish: '
    temp['14']='Non Mutton and Egg: '
    temp['23']='Non Chicken and Fish: '
    temp['24']='Non Chicken and Egg: '
    temp['34']='Non Fish and Egg: '
    temp['123']='Non Mutton and Chicken and Fish: '
    temp['234']='Non Chicken and Fish and Egg: '
    temp['134']='Non Mutton and Fish and Egg: '
    temp['124']='Non Mutton and Chicken and Egg: '
    temp['1234']='Non Mutton and Chicken and Fish and Egg: '
    return temp[string]


class Presence(models.Model):
    HALF_CHOICES = (('MO', 'Morning'),('EV', 'Evening'),)
    boarder = models.ManyToManyField(Boarder, limit_choices_to={'Current_Boarder': True}, blank=True)
    meal_date = models.DateField()
    half = models.CharField(choices=HALF_CHOICES, unique_for_date='meal_date', max_length=12)
    change_by = models.DateTimeField()
    meal_dishes = models.CharField(blank=True, max_length=150)
    has_fish = models.BooleanField(default=False)
    has_chicken = models.BooleanField(default=False)
    has_mutton = models.BooleanField(default=False)
    has_egg = models.BooleanField(default=False)
    extra_meals = models.DecimalField(default=4, decimal_places=0, max_digits=2)
    extra_description = models.TextField(default='')
    adjust_count = models.IntegerField(default=0)
    guest_meal=models.IntegerField(default=0)

    def get_current_half(self):
        if self.half=='MO':
            if datetime.now().hour<13:
                return 1
            else:
                return 2
        else:
            if datetime.now().hour>12:
                return 1
            else:
                return 2

    def get_prev_meal(self):

        if self.half=='MO':
            prev_date = self.meal_date()-datetime.timedelta(days=1)
            prev_meal = Presence.objects.get(meal_date=prev_date, half='EV')
        else:
            prev_meal = Presence.objects.get(meal_date=self.meal_date, half='MO')
        return prev_meal

    def get_absolute_string(self):

        get_value={}
        if self.half=='MO':
            boarder=Boarder.objects.filter(Morning_Presence=True)
        else:
            boarder=Boarder.objects.filter(Evening_Presence=True)

        if self.has_mutton:
            get_value['1']=boarder.filter(Morning_Presence=True, Eats_Mutton = not self.has_mutton).count()
        else:
            get_value['1']=None

        if self.has_chicken:
            get_value['2']=boarder.filter(Morning_Presence=True, Eats_Chicken = not self.has_chicken).count()
        else:
            get_value['2']=None

        if self.has_fish:
            get_value['3']=boarder.filter(Morning_Presence=True, Eats_Fish = not self.has_fish).count()
        else:
            get_value['3']=None

        if self.has_egg:
            get_value['4']=boarder.filter(Morning_Presence=True, Eats_Egg = not self.has_egg).count()
        else:
            get_value['4']=None

        if self.has_mutton and self.has_chicken:
            get_value['12']=boarder.filter(Morning_Presence=True, Eats_Mutton = not self.has_mutton, Eats_Chicken = not self.has_chicken).count()
                
        else:
            get_value['12']=None

        if self.has_mutton and self.has_fish:
            get_value['13']=boarder.filter(Morning_Presence=True, Eats_Mutton = not self.has_mutton, Eats_Fish = not self.has_fish).count()
        else:
            get_value['13']=None

        if self.has_mutton and self.has_egg:
            get_value['14']=boarder.filter(Morning_Presence=True, Eats_Mutton = not self.has_mutton, Eats_Egg = not self.has_egg).count()
        else:
            get_value['14']=None

        if self.has_chicken and self.has_fish:
            get_value['23']=boarder.filter(Morning_Presence=True, Eats_Chicken = not self.has_chicken, Eats_Fish = not self.has_fish).count()
        else:
            get_value['23']=None

        if self.has_chicken and self.has_egg:
            get_value['24']=boarder.filter(Morning_Presence=True, Eats_Chicken = not self.has_chicken, Eats_Egg = not self.has_egg).count()
        else:
            get_value['24']=None

        if self.has_fish and self.has_egg:
            get_value['34']=boarder.filter(Morning_Presence=True, Eats_Fish = not self.has_fish, Eats_Egg = not self.has_egg).count()
        else:
            get_value['34']=None

        if self.has_mutton and self.has_chicken and self.has_fish:
            get_value['123']=boarder.filter(Morning_Presence=True, Eats_Mutton = not self.has_mutton, Eats_Chicken = not self.has_chicken,Eats_Fish = not self.has_fish).count()
        else:
            get_value['123']=None

        if self.has_chicken and self.has_fish and self.has_egg:
            get_value['234']=boarder.filter(Morning_Presence=True, Eats_Chicken = not self.has_chicken, Eats_Fish = not self.has_fish, Eats_Egg = not self.has_egg).count()
        else:
            get_value['234']=None

        if self.has_mutton and self.has_fish and self.has_egg:
            get_value['134']=boarder.filter(Morning_Presence=True, Eats_Mutton = not self.has_mutton, Eats_Fish = not self.has_fish, Eats_Egg = not self.has_egg).count()
        else:
            get_value['134']=None

        if self.has_mutton and self.has_chicken and self.has_egg:
            get_value['124']=boarder.filter(Morning_Presence=True, Eats_Mutton = not self.has_mutton, Eats_Chicken = not self.has_chicken, Eats_Egg = not self.has_egg).count()
        else:
            get_value['124']=None

        if self.has_mutton and self.has_chicken and self.has_fish and self.has_egg:
            get_value['1234']=boarder.filter(Morning_Presence=True, Eats_Mutton = not self.has_mutton, Eats_Chicken = not self.has_chicken,Eats_Fish = not self.has_fish, Eats_Egg = not self.has_egg).count()
        else:
            get_value['1234']=None

        string=""
        for i in range(10):
            try:
                if get_value[str(i+1)] != None:
                    string+=str(i+1)
            except:
                break

        count_string=[]
        iteration=[]
        string_list=[]

        for l in range(1,len(string)+1):
            string_list=generate_length_wise_string(string,string_list,l)

        for generate_string in string_list:
            if get_value[generate_string]-get_value[string]:
                iteration.append([get_value[generate_string]-get_value[string],generate_string])
                #count_string.append(temp[generate_string]+str(self.get_veg_count()[generate_string]-self.get_veg_count()[string]))
        #return count_string

        max_length_string_count=1
        while True:
            try:
                if len(iteration[len(iteration)-max_length_string_count][1])>1:#==len(iteration[len(iteration)-1][1]):
                    remove_count=0
                    for i in range(len(iteration)-max_length_string_count):
                        find_count=0
                        for j in iteration[i-remove_count][1]:
                            if iteration[len(iteration)-max_length_string_count][1].find(j) !=-1:
                                find_count+=1
                            else:
                                break
                        if find_count==len(iteration[i-remove_count][1]):
                            if iteration[i-remove_count][0]-iteration[len(iteration)-max_length_string_count][0]>0:
                                iteration[i-remove_count][0]=iteration[i][0]-iteration[len(iteration)-max_length_string_count][0]
                            else:
                                iteration.remove(iteration[i-remove_count])
                                remove_count+=1
                    max_length_string_count+=1
                else:
                    break
            except:
                break

        for i in iteration:
            count_string.append(get_string(i[1])+str(i[0]))
        try:
            if get_value[string]:
                count_string.append('Veg: '+str(get_value[string]))
            if self.get_total_meals()-get_value[string]:
                count_string.append('Non Veg: '+str(self.get_total_meals()-get_value[string]))
        except:
            pass
        if self.adjust_count:
            count_string.append('Adjustment: '+str(self.adjust_count))

        if self.guest_meal:
            count_string.append('Guest Meal: '+str(self.guest_meal))

        return count_string

    def get_total_meals(self):
        return self.extra_meals-self.adjust_count+self.boarder.count()+self.guest_meal

    def meal_half(self):
        if self.half=='MO':
            return 'Morning'
        else:
            return 'Evening'

    def __str__(self):
        return str(self.meal_date)+self.half


class FutureBoarder(models.Model):
    HALF_CHOICES = (('MO', 'Morning'),
        ('EV', 'Evening'),)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    offdate=models.DateField(blank=True)
    offhalf = models.CharField(choices=HALF_CHOICES,max_length=12,blank=True)
    ondate=models.DateField(blank=True)
    onhalf = models.CharField(choices=HALF_CHOICES,max_length=12,blank=True)   
    def __str__(self):
        return str(self.user)+'---'+str(self.offdate)+'('+self.offhalf+')'+'---'+str(self.ondate)+'('+self.onhalf+')'

class MealDishes(models.Model):
    HALF_CHOICES = (('MO', 'Morning'),
        ('EV', 'Evening'),)
    Meal_Dish = models.CharField(blank=True,max_length=100)
    Meal_Date = models.DateField(blank=True)    
    Meal_Half = models.CharField(choices=HALF_CHOICES,unique_for_date='Meal_Date',max_length=12,blank=True)

    def Half(self):
        if self.Meal_Half=='MO':
            return 'Morning'
        else:
            return 'Evening'
    def __str__(self):
        return str(self.Meal_Dish)+'---'+str(self.Meal_Half)+'---'+str(self.Meal_Date)

class GuestMeal(models.Model):
    HALF_CHOICES = (('MO', 'Morning'),
        ('EV', 'Evening'),)
    user= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    Meal_Date = models.DateField()
    Meal_Half = models.CharField(choices=HALF_CHOICES, max_length=12)
    No_Of_Guest=models.IntegerField(default=0)
    def __str__(self):
        return str(self.user)

class StoreKeeper(models.Model):
    HALF_CHOICES = (('1MO', 'Morning'),
        ('2EV', 'Evening'),)
    Store_Name=models.ForeignKey(Boarder,on_delete=models.CASCADE,blank=True,null=True,limit_choices_to={'Year_Of_Passing':Boarder.objects.aggregate(Year_Of_Passing=Max('Year_Of_Passing'))['Year_Of_Passing'],'Current_Boarder':True},unique_for_date='Store_Date')
    Store_Date = models.DateField()
    Store_Half = models.CharField(choices=HALF_CHOICES, unique_for_date='Store_Date', max_length=12)
    def get_store_half(self):
        if self.Store_Half=='1MO':
            return 'Morning'
        else:
            return 'Evening'
    def __str__(self):
        return str(self.Store_Date)+' ('+self.Store_Half+')'
